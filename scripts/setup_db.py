# scripts/setup_db.py
# Creates the tables in PostgreSQL bank_reviews database

import psycopg2
import sys

DB_CONFIG = {
    "host": "localhost",
    "database": "bank_reviews",
    "user": "postgres",
    "password": "123"
}

def create_tables():
    """Create banks and reviews tables."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("✅ Connected to database successfully!")

        # Create banks table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS banks (
                bank_id SERIAL PRIMARY KEY,
                bank_name VARCHAR(100) UNIQUE NOT NULL,
                app_name VARCHAR(100)
            );
        """)
        print("✅ Banks table created")

        # Create reviews table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id SERIAL PRIMARY KEY,
                bank_id INTEGER REFERENCES banks(bank_id),
                review_text TEXT NOT NULL,
                rating INTEGER CHECK (rating BETWEEN 1 AND 5),
                review_date DATE,
                sentiment_label VARCHAR(20),
                sentiment_score FLOAT,
                identified_theme VARCHAR(100),
                source VARCHAR(50)
            );
        """)
        print("✅ Reviews table created")

        conn.commit()
        cur.close()
        conn.close()
        print("\n✅ Database setup complete!")

    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_tables()