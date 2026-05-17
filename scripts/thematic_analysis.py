# scripts/thematic_analysis.py
# Groups reviews into themes based on keywords

import pandas as pd

# 5 themes with their keywords
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

def assign_theme(text):
    """Assign the best matching theme to a review."""
    text = str(text).lower()
    scores = {}
    for theme, keywords in THEMES.items():
        scores[theme] = sum(1 for kw in keywords if kw in text)
    best_theme = max(scores, key=scores.get)
    return best_theme if scores[best_theme] > 0 else 'General Feedback'

def main():
    # Load sentiment results
    df = pd.read_csv('data/bank_reviews_sentiment.csv')
    print(f"Loaded {len(df)} reviews")

    # Assign themes
    print("Assigning themes...")
    df['identified_theme'] = df['review'].apply(assign_theme)

    # Show results
    print("\n--- Theme Counts per Bank ---")
    print(df.groupby(['bank', 'identified_theme']).size().unstack(fill_value=0))

    print("\n--- Overall Theme Counts ---")
    print(df['identified_theme'].value_counts())

    # Save
    df.to_csv('data/bank_reviews_analyzed.csv', index=False)
    print("\n✅ Saved to data/bank_reviews_analyzed.csv")

if __name__ == "__main__":
    main()