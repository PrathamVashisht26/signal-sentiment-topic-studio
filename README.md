# Signal — Sentiment & Topic Studio

A local web application for exploring sentiment and recurring topics in English social-media posts. Paste text or upload a CSV, analyze it offline, and explore the results in an interactive dashboard.

**No API keys. No paid inference API. No live social-media collection.** Internet is needed only to install dependencies; analysis runs on your computer.

Built by [Pratham Vashisht](https://github.com/PrathamVashisht26).

## Features

- Analyze pasted posts, one per line, or a UTF-8 CSV with a `text` column.
- Explore the included 50-post electric-vehicle example without supplying data.
- Classify each whole post as positive, neutral, or negative using VADER.
- Discover keyword groups using TF-IDF and Non-negative Matrix Factorization (NMF).
- View sentiment distribution, average polarity, topic counts, and individual results.
- Filter the results table by keyword and sentiment; export the complete analysis as CSV.
- Use the built-in **How it works** page for a technical walkthrough.
- Process up to 1,000 non-empty posts, 5,000 characters per post, and 2 MB per upload.

## Quick start

Use Python 3.11. Clone the repository and install dependencies in a virtual environment.

```bash
git clone https://github.com/PrathamVashisht26/signal-sentiment-topic-studio.git
cd signal-sentiment-topic-studio
python -m venv .venv
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

After setup, you can also double-click `start.bat`.

**macOS / Linux:**

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Open **http://127.0.0.1:5000**. Keep the terminal open during your demo; press Ctrl+C to stop. This address works on the machine running the application. The development server is not a public hosting deployment.

If Windows prevents creating a virtual environment under OneDrive, use a normal local development folder.

## How to use it

1. The dashboard starts with a clearly labeled **example dataset**.
2. Paste your own posts and click **Analyze posts**, or switch to **Upload CSV**.
3. Inspect the charts and individual post results.
4. Search for a term such as `battery` to filter the already-analyzed table.
5. Use **Export CSV** to download every analyzed post with its label, compound score, and topic terms.

**Search does not fetch posts from the internet or recalculate the charts.** The charts and export describe the complete analysis, regardless of table filters. Sentiment applies to the whole post, not specifically to the searched keyword.

Example CSV:

```csv
text
"This car is excellent!"
"The battery is not good."
"The new model launches on Tuesday."
```

Additional CSV columns are ignored. Empty entries and exact duplicate text are removed.

## Architecture

```text
Browser: HTML / CSS / JavaScript
              |
       POST /api/analyze
              |
       Flask validation
              |
       Deduplicate posts
          /         \
       VADER       TF-IDF + NMF
          \         /
          JSON response
              |
     Charts / table / CSV export
```

### Sentiment

VADER is a lexicon and rule-based analyzer, not a transformer or generative model. URLs are removed for sentiment scoring, while negation, punctuation, and capitalization are preserved. Its normalized compound score ranges from -1 to +1:

| Score | Label |
| --- | --- |
| >= 0.05 | Positive |
| <= -0.05 | Negative |
| Between these thresholds | Neutral |

Scores measure polarity, **not confidence probabilities**. Example: `This is good` and `This is not good` produce opposite labels.

### Topics

TF-IDF weights English unigrams and bigrams. NMF learns up to five groups with a fixed random seed; each post is assigned to its strongest group. Labels are the highest-weighted terms, not human-authored topic names. Fewer than four posts use top keywords instead. Text with no usable vocabulary retains sentiment results and an unassigned topic.

### Data handling

Text is processed in server memory and returned to your browser. The application makes no outbound analysis requests and stores no uploaded posts in a database. Refreshing resets the dashboard to the example; download a CSV to retain results. Export escapes formula prefixes for safer spreadsheet opening.

## Notebook

`Social_media_project.ipynb` demonstrates the same offline pipeline. From the repository root, install Jupyter separately if needed (`python -m pip install jupyter`) and open the notebook. It no longer requires Tweepy, Gemini, Colab Secrets, or NLTK downloads.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest -v test_app.py
```

Tests cover sample analysis, negation, duplicates, CSV parsing, invalid input, empty vocabulary, upload limits, and static routes. GitHub Actions runs them on Python 3.11. Functional tests do not establish model accuracy.

## Limitations

- English only; sarcasm, slang, mixed sentiment and domain-specific language may be misclassified.
- The sample dataset is for demonstration, not an accuracy benchmark or a live feed.
- Topic groups depend on the uploaded corpus and may overlap or produce weak labels.
- No claim of a measured accuracy percentage; evaluate against human-labeled domain data first.
- The app has no live collector, authentication, persistence, or public hosting configuration.
- Your laptop must remain on while demonstrating the locally hosted website.

## Repository structure

```text
app.py                       Flask API and offline analysis
templates/index.html         Dashboard and pipeline explanation
static/                      JavaScript and styles
data/sample_tweets.csv       50-post EV example
Social_media_project.ipynb   Offline notebook walkthrough
test_app.py                  Integration tests
requirements.txt            Runtime dependencies
start.bat                    Windows launcher after setup
.github/workflows/tests.yml  Automated checks
```

## Project evolution

Previously named **Real-Time Social Media Sentiment & Topic Analysis Engine**, this project depended on X/Twitter access and Gemini inference. Signal replaces those dependencies with an offline website and an explainable NLP baseline. The earlier implementation remains in Git history. Potential future work includes an evaluated transformer backend and a separately labeled live-data collector.

## References and license

- [VADER](https://github.com/cjhutto/vaderSentiment)
- [Scikit-learn topic extraction](https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html)

MIT License. See [LICENSE](LICENSE).
