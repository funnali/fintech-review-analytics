# scripts/thematic_analysis.py
# Theme assignment + integrated TF-IDF keyword extraction

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import sys

THEMES = {
    'Account Access Issues': [
        'login', 'password', 'otp', 'verification', 'sign in',
        'access', 'locked', 'logout', 'session', 'username',
        'forgot', 'reset', 'authenticate', 'pin'
    ],
    'Transaction Performance': [
        'transfer', 'slow', 'fast', 'transaction', 'payment',
        'loading', 'crash', 'speed', 'delay', 'timeout',
        'freeze', 'hang', 'stuck', 'error', 'failed', 'send money'
    ],
    'UI & Design': [
        'interface', 'design', 'easy', 'ui', 'navigation',
        'simple', 'look', 'layout', 'screen', 'button',
        'user friendly', 'beautiful', 'clean', 'confusing', 'update'
    ],
    'Customer Support': [
        'support', 'help', 'service', 'response', 'contact',
        'agent', 'call', 'complaint', 'resolve', 'staff',
        'customer care', 'hotline', 'feedback', 'answer'
    ],
    'Feature Requests': [
        'fingerprint', 'feature', 'add', 'improve', 'need',
        'wish', 'dark mode', 'notification', 'statement',
        'face id', 'biometric', 'english', 'amharic', 'language'
    ]
}

def load_data(path='data/bank_reviews_sentiment.csv'):
    """Load sentiment results with error handling."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        df = pd.read_csv(path)
        print(f"✅ Loaded {len(df)} reviews")
        return df
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def assign_theme(text):
    """Assign best matching theme based on keyword rules."""
    try:
        text = str(text).lower()
        scores = {
            theme: sum(1 for kw in keywords if kw in text)
            for theme, keywords in THEMES.items()
        }
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'General Feedback'
    except Exception:
        return 'General Feedback'

def extract_tfidf_keywords(df, top_n=10):
    """
    Extract top keywords per bank using TF-IDF.
    This systematically surfaces key terms beyond rule-based matching.
    """
    try:
        print("\n--- TF-IDF Keyword Extraction per Bank ---")
        all_keywords = []

        for bank in df['bank'].unique():
            bank_reviews = df[df['bank'] == bank]['review'].fillna('')

            vectorizer = TfidfVectorizer(
                max_features=500,
                stop_words='english',
                ngram_range=(1, 2)
            )
            tfidf_matrix = vectorizer.fit_transform(bank_reviews)
            feature_names = vectorizer.get_feature_names_out()
            mean_scores = tfidf_matrix.mean(axis=0).A1
            top_indices = mean_scores.argsort()[::-1][:top_n]

            print(f"\n{bank}:")
            for idx in top_indices:
                word = feature_names[idx]
                score = round(mean_scores[idx], 4)
                print(f"  {word:<30} {score}")
                all_keywords.append({
                    'bank': bank,
                    'keyword': word,
                    'tfidf_score': score
                })

        # Save keywords
        kw_df = pd.DataFrame(all_keywords)
        kw_df.to_csv('data/tfidf_keywords.csv', index=False)
        print("\n✅ TF-IDF keywords saved to data/tfidf_keywords.csv")
        return kw_df

    except Exception as e:
        print(f"⚠️ TF-IDF extraction failed: {e}")
        return pd.DataFrame()

def compare_rules_vs_tfidf(df, kw_df):
    """
    Compare rule-based theme keywords vs TF-IDF surfaced terms.
    This evaluates reliability of keyword rules.
    """
    try:
        print("\n--- Rule-Based vs TF-IDF Comparison ---")
        all_rule_keywords = set()
        for keywords in THEMES.values():
            all_rule_keywords.update(keywords)

        for bank in df['bank'].unique():
            bank_kw = kw_df[kw_df['bank'] == bank]['keyword'].tolist()
            matches = [kw for kw in bank_kw if any(
                rule in kw or kw in rule
                for rule in all_rule_keywords
            )]
            coverage = (len(matches) / len(bank_kw)) * 100 if bank_kw else 0
            print(f"{bank}: {len(matches)}/{len(bank_kw)} TF-IDF terms "
                  f"matched rule keywords ({coverage:.0f}% overlap)")
    except Exception as e:
        print(f"⚠️ Comparison failed: {e}")

def main():
    df = load_data()

    # Rule-based theme assignment
    print("\nAssigning themes...")
    df['identified_theme'] = df['review'].apply(assign_theme)

    print("\n--- Theme Counts per Bank ---")
    print(df.groupby(['bank', 'identified_theme']).size().unstack(fill_value=0))

    # TF-IDF keyword extraction
    kw_df = extract_tfidf_keywords(df, top_n=10)

    # Compare rules vs TF-IDF
    if not kw_df.empty:
        compare_rules_vs_tfidf(df, kw_df)

    # Save final output
    try:
        df.to_csv('data/bank_reviews_analyzed.csv', index=False)

        # Task 2 required output format
        task2 = df[['review_id', 'review', 'sentiment_label',
                    'sentiment_score', 'identified_theme']]
        task2.columns = ['review_id', 'review_text', 'sentiment_label',
                         'sentiment_score', 'identified_theme']
        task2.to_csv('data/task2_final_output.csv', index=False)

        print("\n✅ Saved bank_reviews_analyzed.csv")
        print("✅ Saved task2_final_output.csv")
    except Exception as e:
        print(f"❌ Error saving: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()