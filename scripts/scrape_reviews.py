from google_play_scraper import reviews, Sort
import pandas as pd

apps = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

all_reviews = []

for bank, app_id in apps.items():
    print(f"Scraping reviews for {bank}...")

    result, continuation_token = reviews(
        app_id,
        lang='en',
        country='et',
        sort=Sort.NEWEST,
        count=500
    )

    for review in result:
        all_reviews.append({
            "review": review['content'],
            "rating": review['score'],
            "date": review['at'].strftime('%Y-%m-%d'),
            "bank": bank,
            "source": "Google Play"
        })

df = pd.DataFrame(all_reviews)

print(df.head())

print(f"\nTotal reviews collected: {len(df)}")

df.to_csv("data/bank_reviews_raw.csv", index=False)

print("\nRaw review dataset saved successfully.")