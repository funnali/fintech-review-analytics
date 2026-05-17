# scripts/tfidf_keywords.py
# Extracts top keywords per bank using TF-IDF
# This satisfies the Task 2 requirement for keyword extraction

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def get_top_keywords(text_series, top_n=15):
    """Extract top N keywords from a series of reviews using TF-IDF."""
    vectorizer = TfidfVectorizer(
        max_features=500,
        stop_words='english',
        ngram_range=(1, 2)  # includes both single words and 2-word phrases
    )
    tfidf_matrix = vectorizer.fit_transform(text_series.fillna(''))
    feature_names = vectorizer.get_feature_names_out()
    mean_scores = tfidf_matrix.mean(axis=0).A1
    top_indices = mean_scores.argsort()[::-1][:top_n]
    return [(feature_names[i], round(mean_scores[i], 4)) for i in top_indices]

def main():
    df = pd.read_csv('data/bank_reviews_analyzed.csv')

    print("=" * 60)
    print("TF-IDF TOP KEYWORDS PER BANK")
    print("=" * 60)

    all_keywords = []

    for bank in df['bank'].unique():
        bank_reviews = df[df['bank'] == bank]['review']
        keywords = get_top_keywords(bank_reviews, top_n=15)

        print(f"\n--- {bank} ---")
        for word, score in keywords:
            print(f"  {word:<30} {score}")
            all_keywords.append({
                'bank': bank,
                'keyword': word,
                'tfidf_score': score
            })

    # Save keywords to CSV
    kw_df = pd.DataFrame(all_keywords)
    kw_df.to_csv('data/tfidf_keywords.csv', index=False)
    print("\n✅ Keywords saved to data/tfidf_keywords.csv")

    # Also show sentiment aggregated by star rating
    print("\n" + "=" * 60)
    print("MEAN SENTIMENT SCORE BY STAR RATING")
    print("=" * 60)
    rating_sentiment = df.groupby(['bank', 'rating'])['sentiment_score'].mean().round(3)
    print(rating_sentiment)

    # Save this too
    rating_sentiment.to_csv('data/sentiment_by_rating.csv')
    print("\n✅ Sentiment by rating saved to data/sentiment_by_rating.csv")

if __name__ == "__main__":
    main()