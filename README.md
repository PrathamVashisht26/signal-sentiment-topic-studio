# Real-Time Social Media Sentiment & Topic Analysis Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Colab](https://img.shields.io/badge/Open%20In-Colab-orange?logo=google-colab)
![NLP](https://img.shields.io/badge/NLP-NLTK-green)
![AI](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-purple?logo=google)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A complete end-to-end NLP pipeline that ingests social media posts, cleans raw text using advanced preprocessing, and uses **Google Gemini 1.5 Flash** to extract structured **sentiment** and **topic** information from each post — producing actionable insights with visualizations.

---

## Problem It Solves

Manually reading hundreds of social media posts to understand public opinion is impractical. This engine automates that process: given any keyword or topic, it fetches posts, cleans the noisy social media text, and classifies each post by sentiment and subject — in minutes.

**Use cases:**
- Track brand perception on social media
- Monitor public opinion on news events
- Analyse customer feedback at scale
- Research public discourse around any topic

---

## Pipeline Architecture

```
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  STEP 1             │     │  STEP 2               │     │  STEP 3             │     │  STEP 4             │
│  Data Ingestion     │────▶│  Text Preprocessing  │────▶│  AI Analysis        │────▶│  Visualization      │
│  Twitter API v2     │     │  (NLTK + Regex +      │     │  (Gemini 1.5 Flash) │     │  (Matplotlib)       │
│  or Sample Dataset  │     │   Lemmatization)      │     │  Sentiment + Topic  │     │  Charts & Insights  │
└─────────────────────┘     └──────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Social Data | Tweepy (Twitter API v2) |
| Text Processing | NLTK, Regex, Emoji |
| AI Analysis | Google Gemini 1.5 Flash |
| Data Handling | Pandas |
| Visualization | Matplotlib |
| Runtime | Google Colab / Jupyter |

---

## Features

- **Smart data ingestion** — Connects to Twitter API v2; automatically falls back to included sample dataset if API is unavailable
- **Advanced NLP preprocessing pipeline** — Emoji demojization → URL removal → mention stripping → lemmatization → stopword removal
- **LLM-powered analysis** — Uses Gemini 1.5 Flash to label sentiment (Positive / Negative / Neutral) and extract a topic phrase per tweet
- **Structured JSON output** — Gemini responses are parsed and validated before saving
- **Visualization dashboard** — Sentiment distribution bar chart + Top-10 topics horizontal bar chart
- **Fully runnable without paid APIs** — Included sample dataset of 50 Electric Vehicle tweets lets you demo the entire pipeline for free

---

## Project Structure

```
├── Social_media_project.ipynb   ← Main notebook (run this)
├── requirements.txt             ← Python dependencies
├── .env.example                 ← API key template
├── data/
│   └── sample_tweets.csv        ← 50 sample EV tweets (no API needed)
└── README.md
```

---

## Quick Start

### Option A — Google Colab (Recommended)

1. Click the **Open in Colab** badge at the top of the notebook
2. Add your API keys to **Colab Secrets** (🔑 icon in the left sidebar):
   - `GEMINI_API_KEY` — required for sentiment analysis *(free)*
   - `BEARER_TOKEN` — optional, for live Twitter data *(paid plan required)*
3. Click **Runtime → Run All**

The notebook automatically uses the included `data/sample_tweets.csv` if no Twitter token is provided.

### Option B — Local (Jupyter)

```bash
# 1. Clone the repository
git clone https://github.com/PrathamVashisht26/Real-Time-Social-Media-Sentiment-Topic-Analysis-Engine-.git
cd Real-Time-Social-Media-Sentiment-Topic-Analysis-Engine-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up API keys
cp .env.example .env
# Edit .env and add your keys

# 4. Launch the notebook
jupyter notebook Social_media_project.ipynb
```

---

## API Keys

### Google Gemini API Key (FREE)
1. Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Add it to Colab Secrets as `GEMINI_API_KEY`

### Twitter Bearer Token (OPTIONAL — paid)
> **Note:** Twitter's v2 `search_recent_tweets` endpoint requires a **paid Basic tier** subscription ($100/month as of 2024). The free developer account no longer includes this access.
> 
> The project includes a sample dataset so you can run and demo the full pipeline without this.

1. Go to [developer.twitter.com/en/portal/dashboard](https://developer.twitter.com/en/portal/dashboard)
2. Create a project and app
3. Copy the **Bearer Token**
4. Add it to Colab Secrets as `BEARER_TOKEN`

---

## Sample Output

The notebook produces:
- `cleaned_tweets.csv` — preprocessed text ready for analysis
- `analyzed_tweets.csv` — tweets with `sentiment` and `topic` columns added
- `sentiment_analysis_results.png` — visualization chart

**Example analyzed row:**

| text | sentiment | topic |
|---|---|---|
| "just drove tesla model mile single charge electric vehicle amazing" | Positive | EV Range |
| "charging infrastructure electric vehicle nightmare waited minute broken charger" | Negative | Charging Issues |
| "new study ev significantly lower lifetime emission gasoline car interesting data" | Neutral | EV Emissions |

---

## Known Limitations

| Limitation | Details |
|---|---|
| Twitter API access | Free tier no longer supports tweet search; paid plan required for live data |
| Gemini quota | Free tier has per-minute rate limits; notebook adds `0.5s` delay between calls |
| Analysis scope | Capped at 20 tweets for Gemini analysis to stay within free quota |
| Language | Preprocessing optimised for English tweets only |

---

## Author

**Pratham Vashisht**  
[GitHub](https://github.com/PrathamVashisht26)

---

## License

This project is licensed under the MIT License.
