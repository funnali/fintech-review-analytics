# scripts/top_up_reviews.py
# Tops up reviews to reach 400+ per bank

from google_play_scraper import reviews, Sort
import pandas as pd

APPS = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.dashen.dashensuperapp'
}

# Load existing cleaned data
existing = pd.read_csv('data/bank_reviews_cleaned.csv')
print('Existing counts:')
print(existing['bank'].value_counts())

# Scrape extra reviews
extra = []
for bank, app_id in APPS.items():
    print(f"\nScraping extra reviews for {bank}...")
    result, _ = reviews(
        app_id,
        lang='en',
        country='et',
        sort=Sort.NEWEST,
        count=450
    )
    for r in result:
        extra.append({
            'review': r['content'],
            'rating': r['score'],
            'date': r['at'].strftime('%Y-%m-%d'),
            'bank': bank,
            'source': 'Google Play'
        })
    print(f"  Got {len(result)} reviews")

# Combine old + new
new_df = pd.DataFrame(extra)
combined = pd.concat([existing, new_df], ignore_index=True)

# Clean
combined.drop_duplicates(subset=['review'], inplace=True)
combined.dropna(subset=['review', 'rating'], inplace=True)
combined = combined[['review', 'rating', 'date', 'bank', 'source']]

# Save
combined.to_csv('data/bank_reviews_cleaned.csv', index=False)

print('\n✅ Updated counts:')
print(combined['bank'].value_counts())
print(f'\nTotal: {len(combined)}')