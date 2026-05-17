import pandas as pd

# Load raw dataset
df = pd.read_csv("data/bank_reviews_raw.csv")

print("Initial dataset shape:")
print(df.shape)

# Remove duplicate reviews
before_duplicates = len(df)

df = df.drop_duplicates(subset=["review"])

after_duplicates = len(df)

duplicates_removed = before_duplicates - after_duplicates

print(f"\nDuplicates removed: {duplicates_removed}")

# Remove missing review or rating rows
before_missing = len(df)

df = df.dropna(subset=["review", "rating"])

after_missing = len(df)

missing_removed = before_missing - after_missing

print(f"Rows removed due to missing values: {missing_removed}")

# Standardize date format
df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

# Remove empty review text
df = df[df["review"].str.strip() != ""]

# Final dataset info
print("\nFinal dataset shape:")
print(df.shape)

# Save cleaned dataset
df.to_csv("data/bank_reviews_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully.")