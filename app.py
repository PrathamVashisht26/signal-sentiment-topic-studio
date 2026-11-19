"""Local sentiment workbench. No outbound requests or paid APIs."""
import csv
import io
import re
from pathlib import Path
from collections import Counter

from flask import Flask, jsonify, render_template, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
analyzer = SentimentIntensityAnalyzer()
ROOT = Path(__file__).parent


def analyze(texts, source):
    if not texts:
        raise ValueError('Add at least one non-empty post.')
    if len(texts) > 1000:
        raise ValueError('Please use at most 1,000 posts per analysis.')
    if any(len(t) > 5000 for t in texts):
        raise ValueError('Each post must be 5,000 characters or fewer.')
    original_count = len(texts)
    texts = list(dict.fromkeys(texts))
    rows = []
    for text in texts:
        scores = analyzer.polarity_scores(re.sub(r'https?://\S+', '', text))
        compound = scores['compound']
        label = 'Positive' if compound >= .05 else 'Negative' if compound <= -.05 else 'Neutral'
        rows.append(dict(text=text, sentiment=label, score=compound, topic='Unassigned'))
    topics = []
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1500, ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(texts)
        terms = vectorizer.get_feature_names_out()
        if len(texts) < 4:
            label = ' / '.join(terms[matrix.sum(axis=0).A1.argsort()[-3:][::-1]])
            for row in rows:
                row['topic'] = label
            topics = [dict(name=label, count=len(rows))]
        else:
            count = min(5, max(2, len(texts) // 8), matrix.shape[1], len(texts))
            model = NMF(n_components=count, init='nndsvda', random_state=42, max_iter=500)
            weights = model.fit_transform(matrix)
            names = [' / '.join(terms[c.argsort()[-3:][::-1]]) for c in model.components_]
            for row, weight in zip(rows, weights):
                row['topic'] = names[weight.argmax()] if weight.max() > 0 else 'Unassigned'
            topics = [dict(name=name, count=n) for name, n in Counter(r['topic'] for r in rows).most_common()]
    except ValueError:
        pass  # Empty vocabulary: sentiment results are still useful.
    counts = {label: sum(r['sentiment'] == label for r in rows) for label in ['Positive', 'Neutral', 'Negative']}
    return dict(rows=rows, topics=topics, counts=counts, total=len(rows), duplicates=original_count-len(rows), source=source,
                average=round(sum(r['score'] for r in rows)/len(rows), 3), engine='VADER', topic_engine='TF-IDF + NMF')


@app.get('/')
def home():
    return render_template('index.html')


@app.post('/api/analyze')
def analysis():
    try:
        if 'file' in request.files:
            file = request.files['file']
            try:
                reader = csv.DictReader(io.StringIO(file.read().decode('utf-8-sig')))
                if not reader.fieldnames or 'text' not in reader.fieldnames:
                    raise ValueError('Your CSV needs a column named text. Save it using UTF-8 encoding.')
                texts = []
                for row in reader:
                    value = (row.get('text') or '').strip()
                    if value:
                        texts.append(value)
                    if len(texts) > 1000:
                        raise ValueError('Please use at most 1,000 non-empty posts.')
            except UnicodeDecodeError:
                raise ValueError('Please save your CSV with UTF-8 encoding.')
            source = 'Uploaded CSV'
        else:
            data = request.get_json(silent=True)
            if not isinstance(data, dict):
                raise ValueError('Send a JSON object with text, or upload a CSV file.')
            if data.get('sample'):
                with (ROOT / 'data' / 'sample_tweets.csv').open(encoding='utf-8-sig', newline='') as f:
                    texts = [r['text'] for r in csv.DictReader(f)]
                source = 'Example dataset · Electric vehicles'
            else:
                value = data.get('text', '')
                if not isinstance(value, str):
                    raise ValueError('Text input must be a string.')
                texts = [t.strip() for t in value.splitlines() if t.strip()]
                source = 'Pasted text'
        return jsonify(analyze(texts, source))
    except (ValueError, csv.Error) as error:
        return jsonify(error=str(error)), 400


@app.errorhandler(413)
def too_large(error):
    return jsonify(error='File too large. Maximum upload size is 2 MB.'), 413


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
