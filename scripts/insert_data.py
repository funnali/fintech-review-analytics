# scripts/insert_data.py
# Inserts cleaned and analyzed review data into PostgreSQL

import psycopg2
import pandas as pd
import sys
import os

DB_CONFIG = {
    "host": "localhost",
    "database": "bank_reviews",
    "user": "postgres",
    "password": "123"
}

BANKS = {
    "CBE": "Commercial Bank of Ethiopia Mobile",
    "BOA": "Bank of Abyssinia Mobile",
    "Dashen": "Dashen Bank Super App"
}

def load_data(path='data/bank_reviews_analyzed.csv'):
    """Load analyzed reviews with error handling."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        df = pd.read_csv(path)
        print(f"✅ Loaded {len(df)} reviews from {path}")
        return df
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        sys.exit(1)

def insert_banks(cur):
    """Insert bank records."""
    for bank_name, app_name in BANKS.items():
        cur.execute("""
            INSERT INTO banks (bank_name, app_name)
            VALUES (%s, %s)
            ON CONFLICT (bank_name) DO NOTHING
        """, (bank_name, app_name))
    print("✅ Banks inserted")

def get_bank_id(cur, bank_name):
    """Get bank_id for a given bank name."""
    cur.execute(
        "SELECT bank_id FROM banks WHERE bank_name = %s",
        (bank_name,)
    )
    result = cur.fetchone()
    return result[0] if result else None

def insert_reviews(cur, df):
    """Insert all reviews into database."""
    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        try:
            bank_id = get_bank_id(cur, str(row['bank']))
            if bank_id is None:
                skipped += 1
                continue

            cur.execute("""
                INSERT INTO reviews (
                    bank_id, review_text, rating, review_date,
                    sentiment_label, sentiment_score,
                    identified_theme, source
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                bank_id,
                str(row['review']),
                int(row['rating']),
                str(row['date']),
                str(row['sentiment_label']),
                float(row['sentiment_score']),
                str(row['identified_theme']),
                str(row['source'])
            ))
            inserted += 1

        except Exception as e:
            skipped += 1
            continue

    return inserted, skipped

def verify_data(cur):
    """Run verification queries."""
    print("\n--- Verification Queries ---")

    # Count per bank
    cur.execute("""
        SELECT b.bank_name, COUNT(r.review_id) as review_count
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_name
        ORDER BY review_count DESC;
    """)
    print("\nReviews per bank:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]} reviews")

    # Average rating per bank
    cur.execute("""
        SELECT b.bank_name, ROUND(AVG(r.rating)::numeric, 2) as avg_rating
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_name
        ORDER BY avg_rating DESC;
    """)
    print("\nAverage rating per bank:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]} stars")

    # Check for nulls
    cur.execute("""
        SELECT
            SUM(CASE WHEN review_text IS NULL THEN 1 ELSE 0 END) as null_reviews,
            SUM(CASE WHEN rating IS NULL THEN 1 ELSE 0 END) as null_ratings,
            SUM(CASE WHEN sentiment_label IS NULL THEN 1 ELSE 0 END) as null_sentiment
        FROM reviews;
    """)
    nulls = cur.fetchone()
    print(f"\nNull checks:")
    print(f"  Null review_text: {nulls[0]}")
    print(f"  Null ratings: {nulls[1]}")
    print(f"  Null sentiment: {nulls[2]}")

def main():
    df = load_data()

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("✅ Connected to database!")

        # Insert banks
        insert_banks(cur)

        # Insert reviews
        print(f"\nInserting {len(df)} reviews...")
        inserted, skipped = insert_reviews(cur, df)

        conn.commit()
        print(f"✅ Inserted: {inserted} reviews")
        print(f"⚠️ Skipped: {skipped} reviews")

        # Verify
        verify_data(cur)

        cur.close()
        conn.close()
        print("\n✅ Database insertion complete!")

    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()