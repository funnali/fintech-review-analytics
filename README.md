# Fintech Review Analytics

Customer experience analytics pipeline for Ethiopian mobile banking apps
using Google Play Store reviews — 10 Academy Week 2 Challenge.

## Objective

Analyze customer reviews for three Ethiopian banks to uncover sentiment
trends, recurring themes, and actionable product recommendations.

Banks analyzed:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

## Scraping Methodology

- Tool: `google-play-scraper` Python library
- Source: Google Play Store
- Language filter: English (`lang='en'`)
- Country filter: Ethiopia (`country='et'`)
- Sort: Newest reviews first
- Target: 400+ reviews per bank (1,200+ total)
- Date range: Most recent reviews up to May 2026
- Fields collected: review text, star rating (1–5), date, bank name, source

### Limitations

- Only English-language reviews were scraped; Amharic reviews were excluded
  which may underrepresent certain user segments.
- google-play-scraper may return fewer than 400 reviews per bank if the app
  has limited English reviews. In that case the date range was expanded.
- Review counts: CBE (376), BOA (378), Dashen (383) = 1,137 total.

## Pipeline Steps

1. Scrape reviews → `scripts/scrape_reviews.py`
2. Preprocess & clean → `scripts/preprocess_reviews.py`
3. Sentiment analysis (VADER) → `scripts/sentiment_analysis.py`
4. Thematic analysis → `scripts/thematic_analysis.py`
5. TF-IDF keyword extraction → `scripts/tfidf_keywords.py`
6. Visualizations → `scripts/visualize.py`
7. Database insertion → `scripts/setup_db.py` + `scripts/insert_data.py`

## Sentiment Tool Selection

VADER (Valence Aware Dictionary and sEntiment Reasoner) was selected over
the DistilBERT transformer model for the following reasons:
- No internet download required (works fully offline)
- Processes 1,000+ reviews in under 60 seconds
- Well-suited for short informal text like app reviews
- Compound score maps cleanly to positive/neutral/negative labels

DistilBERT was attempted but failed to download on the target machine due
to network limitations. VADER results were validated against star ratings
and showed strong agreement (5-star reviews = positive, 1-star = negative).

## Key Findings

- CBE: highest average rating (3.92 stars), most positive sentiment
- BOA: lowest average rating (3.23 stars), most negative sentiment
- Dashen: strong UI feedback, declining sentiment trend in early 2026

## Tech Stack

- Python 3.11
- pandas, numpy
- google-play-scraper
- vaderSentiment
- scikit-learn (TF-IDF)
- spaCy
- matplotlib, seaborn
- PostgreSQL + psycopg2
- GitHub Actions (CI/CD)

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Running the Pipeline

```bash
python scripts/scrape_reviews.py
python scripts/preprocess_reviews.py
python scripts/sentiment_analysis.py
python scripts/thematic_analysis.py
python scripts/tfidf_keywords.py
python scripts/visualize.py
python scripts/setup_db.py
python scripts/insert_data.py
```

## Project Structure

```
fintech-review-analytics/
├── .github/workflows/unittests.yml
├── data/                          # excluded from git
├── scripts/                       # all pipeline scripts
├── src/                           # reusable modules
├── tests/                         # unit tests
├── notebooks/                     # analysis notebooks
├── schema.sql                     # database schema
├── requirements.txt
└── README.md
## Database Setup (Task 3)

### Prerequisites
- PostgreSQL 18 installed and running
- Database created: `bank_reviews`

### Create the Database
```bash
psql -U postgres -c "CREATE DATABASE bank_reviews;"
```

### Create Tables
```bash
python scripts/setup_db.py
```

### Insert Data
```bash
python scripts/insert_data.py
```

### Schema
Two tables are used:

**banks** table:
- bank_id (PRIMARY KEY)
- bank_name (UNIQUE)
- app_name

**reviews** table:
- review_id (PRIMARY KEY)
- bank_id (FOREIGN KEY → banks)
- review_text
- rating (1–5)
- review_date
- sentiment_label
- sentiment_score
- identified_theme
- source

### Verification Results
After insertion, verification queries confirmed:
- CBE: 377 reviews, avg rating 3.93 stars
- BOA: 378 reviews, avg rating 3.23 stars  
- Dashen: 383 reviews, avg rating 3.68 stars
- Total: 1,138 reviews inserted
- Null review_text: 0
- Null ratings: 0
- Null sentiment: 0