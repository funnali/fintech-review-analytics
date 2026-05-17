# scripts/generate_task2_output.py
# Generates the final required Task 2 CSV output

import pandas as pd

# Load the analyzed data
df = pd.read_csv('data/bank_reviews_analyzed.csv')

# Create the required output format
task2_output = pd.DataFrame()
task2_output['review_id'] = df['review_id']
task2_output['review_text'] = df['review']
task2_output['bank'] = df['bank']
task2_output['rating'] = df['rating']
task2_output['sentiment_label'] = df['sentiment_label']
task2_output['sentiment_score'] = df['sentiment_score']
task2_output['identified_theme'] = df['identified_theme']

# Save it
task2_output.to_csv('data/task2_final_output.csv', index=False)

# Show a preview
print("✅ Task 2 Final Output created!")
print(f"Total reviews: {len(task2_output)}")
print("\nFirst 5 rows preview:")
print(task2_output[['review_text','sentiment_label','identified_theme']].head())
print("\nSentiment counts:")
print(task2_output['sentiment_label'].value_counts())
print("\nTheme counts:")
print(task2_output['identified_theme'].value_counts())