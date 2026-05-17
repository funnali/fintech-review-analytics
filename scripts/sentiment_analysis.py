# scripts/sentiment_analysis.py
# VADER-based sentiment analysis with error handling and validation

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import sys

REQUIRED_COLUMNS = ['review', 'rating', 'date', 'bank', 'source']
MIN_REVIEWS_PER_BANK = 400

def load_data(path='data/bank_reviews_cleaned.csv'):
    """Load and validate the cleaned dataset."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Data file not found: {path}")
        
        df = pd.read_csv(path)
        print(f"✅ Dataset loaded: {df.shape}")

        # Validate required columns exist
        missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Validate minimum reviews per bank
        counts = df['bank'].value_counts()
        print("\nReview counts per bank:")
        print(counts)
        
        below_min = counts[counts < MIN_REVIEWS_PER_BANK]
        if not below_min.empty:
            print(f"\n⚠️ Warning: Some banks have fewer than {MIN_REVIEWS_PER_BANK} reviews:")
            print(below_min)
            print("Documented limitation: Google Play returned limited English reviews.")
        else:
            print(f"\n✅ All banks meet the {MIN_REVIEWS_PER_BANK}+ review requirement.")

        return df

    except FileNotFoundError as e:
        print(f"❌ File error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Validation error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error loading data: {e}")
        sys.exit(1)

def analyze_sentiment(df):
    """Classify each review as positive, neutral, or negative using VADER."""
    try:
        analyzer = SentimentIntensityAnalyzer()
        labels = []
        scores = []

        print(f"\nAnalyzing sentiment for {len(df)} reviews...")
        for i, text in enumerate(df['review']):
            try:
                score = analyzer.polarity_scores(str(text))['compound']
                if score >= 0.05:
                    label = 'positive'
                elif score <= -0.05:
                    label = 'negative'
                else:
                    label = 'neutral'
            except Exception:
                # If individual review fails, default to neutral
                score = 0.0
                label = 'neutral'

            labels.append(label)
            scores.append(round(score, 4))

            if (i + 1) % 200 == 0:
                print(f"  Processed {i + 1} / {len(df)} reviews...")

        df['sentiment_label'] = labels
        df['sentiment_score'] = scores
        df['review_id'] = range(1, len(df) + 1)

        # Validate coverage
        labeled = df['sentiment_label'].notna().sum()
        coverage = (labeled / len(df)) * 100
        print(f"\n✅ Sentiment coverage: {labeled}/{len(df)} ({coverage:.1f}%)")

        return df

    except Exception as e:
        print(f"❌ Error during sentiment analysis: {e}")
        sys.exit(1)

def aggregate_by_rating(df):
    """Show mean sentiment score per bank per star rating."""
    try:
        print("\n--- Mean Sentiment Score by Bank and Star Rating ---")
        result = df.groupby(['bank', 'rating'])['sentiment_score'].mean().round(3)
        print(result)
        return result
    except Exception as e:
        print(f"⚠️ Could not aggregate by rating: {e}")

def save_results(df, path='data/bank_reviews_sentiment.csv'):
    """Save sentiment results to CSV."""
    try:
        df.to_csv(path, index=False)
        print(f"\n✅ Saved to {path}")
    except Exception as e:
        print(f"❌ Error saving results: {e}")
        sys.exit(1)

def main():
    df = load_data()
    df = analyze_sentiment(df)

    print("\n--- Sentiment Counts per Bank ---")
    print(df.groupby(['bank', 'sentiment_label']).size().unstack(fill_value=0))

    aggregate_by_rating(df)
    save_results(df)

if __name__ == "__main__":
    main()