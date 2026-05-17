# scripts/sentiment_analysis.py
# Uses VADER for fast, offline sentiment analysis (no download needed)

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

def load_data(path='data/bank_reviews_cleaned.csv'):
    df = pd.read_csv(path)
    print(f"Dataset loaded successfully. {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nBanks found: {df['bank'].unique()}")
    return df

def analyze_sentiment(df):
    analyzer = SentimentIntensityAnalyzer()

    labels = []
    scores = []

    print(f"\nAnalyzing {len(df)} reviews... please wait.")
    for i, text in enumerate(df['review']):
        score = analyzer.polarity_scores(str(text))['compound']
        if score >= 0.05:
            label = 'positive'
        elif score <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        labels.append(label)
        scores.append(round(score, 4))

        if (i + 1) % 200 == 0:
            print(f"  Processed {i + 1} / {len(df)} reviews...")

    df['sentiment_label'] = labels
    df['sentiment_score'] = scores
    df['review_id'] = range(1, len(df) + 1)
    return df

def main():
    df = load_data()
    df = analyze_sentiment(df)

    print("\n--- Sentiment Counts per Bank ---")
    print(df.groupby(['bank', 'sentiment_label']).size().unstack(fill_value=0))

    print("\n--- Overall Sentiment Counts ---")
    print(df['sentiment_label'].value_counts())

    # Save to same data/ folder
    output_path = 'data/bank_reviews_sentiment.csv'
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved to {output_path}")

if __name__ == "__main__":
    main()