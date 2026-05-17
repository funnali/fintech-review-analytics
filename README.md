# Fintech Review Analytics

Customer experience analytics pipeline for Ethiopian mobile banking applications using Google Play Store reviews.

## Objective

This project analyzes customer reviews from:

- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

The pipeline includes:

- Review scraping
- Data preprocessing
- Sentiment analysis
- Thematic analysis
- PostgreSQL database integration
- Data visualization
- Business recommendations

## Tech Stack

- Python
- pandas
- google-play-scraper
- transformers
- PostgreSQL
- matplotlib
- seaborn
- GitHub Actions

## Project Structure

```text
fintech-review-analytics/
## Data Collection Methodology

Reviews were scraped from the Google Play Store using the `google-play-scraper` Python library.

### Target Applications
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

### Collected Fields
- Review text
- Rating
- Review date
- Bank name
- Source platform

### Preprocessing Steps
- Removed duplicate reviews
- Removed rows with missing review text or ratings
- Standardized dates to YYYY-MM-DD format
- Exported cleaned dataset for downstream NLP analysis

### Dataset Summary
- Total raw reviews collected: 1500+
- Cleaned dataset prepared for sentiment analysis

### Limitations
Some reviews may contain multilingual text, emojis, spelling inconsistencies, or short responses that can affect NLP accuracy.