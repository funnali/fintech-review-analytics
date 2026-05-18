# scripts/visualize.py
# Creates all charts for the final report

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data
df = pd.read_csv('data/bank_reviews_analyzed.csv')

# Create plots folder
os.makedirs('data/plots', exist_ok=True)

# ─────────────────────────────────────────
# PLOT 1: Sentiment Distribution by Bank
# ─────────────────────────────────────────
sentiment_counts = df.groupby(
    ['bank', 'sentiment_label']
).size().unstack(fill_value=0)

# Make sure all 3 columns exist
for col in ['positive', 'neutral', 'negative']:
    if col not in sentiment_counts.columns:
        sentiment_counts[col] = 0

sentiment_counts = sentiment_counts[['positive', 'neutral', 'negative']]

fig, ax = plt.subplots(figsize=(10, 6))
sentiment_counts.plot(
    kind='bar',
    stacked=True,
    color=['#2ecc71', '#95a5a6', '#e74c3c'],
    ax=ax
)
ax.set_title('Sentiment Distribution by Bank', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Bank', fontsize=12)
ax.set_ylabel('Number of Reviews', fontsize=12)
ax.legend(title='Sentiment', fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=15)
for container in ax.containers:
    ax.bar_label(container, label_type='center', fontsize=9, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig('data/plots/plot1_sentiment_distribution.png', dpi=150)
plt.close()
print("✅ Plot 1 saved — Sentiment Distribution")

# ─────────────────────────────────────────
# PLOT 2: Average Rating per Bank
# ─────────────────────────────────────────
avg_rating = df.groupby('bank')['rating'].mean().sort_values()

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(avg_rating.index, avg_rating.values, color=['#e74c3c', '#f39c12', '#2ecc71'])
ax.set_title('Average Star Rating per Bank', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Average Rating (out of 5)', fontsize=12)
ax.set_xlim(0, 5)
for i, v in enumerate(avg_rating.values):
    ax.text(v + 0.05, i, f'{v:.2f} stars', va='center', fontsize=11)
plt.tight_layout()
plt.savefig('data/plots/plot2_average_ratings.png', dpi=150)
plt.close()
print("✅ Plot 2 saved — Average Ratings")

# ─────────────────────────────────────────
# PLOT 3: Theme Frequency per Bank
# ─────────────────────────────────────────
theme_counts = df.groupby(
    ['bank', 'identified_theme']
).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(12, 7))
theme_counts.T.plot(kind='barh', ax=ax, colormap='Set2')
ax.set_title('Review Themes per Bank', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Number of Reviews', fontsize=12)
ax.set_ylabel('Theme', fontsize=12)
ax.legend(title='Bank', fontsize=10)
plt.tight_layout()
plt.savefig('data/plots/plot3_themes.png', dpi=150)
plt.close()
print("✅ Plot 3 saved — Theme Frequency")

# ─────────────────────────────────────────
# PLOT 4: Rating Distribution Box Plot
# ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df, x='bank', y='rating', hue='bank', palette='Set2', legend=False, ax=ax)
ax.set_title('Rating Distribution per Bank', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Bank', fontsize=12)
ax.set_ylabel('Star Rating', fontsize=12)
ax.tick_params(axis='x', labelrotation=15)
plt.tight_layout()
plt.savefig('data/plots/plot4_rating_boxplot.png', dpi=150)
plt.close()
print("✅ Plot 4 saved — Rating Boxplot")

# ─────────────────────────────────────────
# PLOT 5: Sentiment Score Over Time
# ─────────────────────────────────────────
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M').astype(str)

monthly = df.groupby(
    ['month', 'bank']
)['sentiment_score'].mean().unstack(fill_value=0)

# Keep last 12 months only
monthly = monthly.tail(12)

fig, ax = plt.subplots(figsize=(13, 6))
for bank in monthly.columns:
    ax.plot(monthly.index, monthly[bank], marker='o', label=bank, linewidth=2)
ax.set_title('Average Sentiment Score Over Time (Last 12 Months)',
             fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Average Sentiment Score', fontsize=12)
ax.legend(title='Bank', fontsize=10)
ax.tick_params(axis='x', rotation=45)
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('data/plots/plot5_sentiment_over_time.png', dpi=150)
plt.close()
print("✅ Plot 5 saved — Sentiment Over Time")

print("\n✅ All 5 plots saved to data/plots/")
print("Open the data/plots/ folder to view them!")
# ─────────────────────────────────────────
# PLOT 6: Pain Points per Bank (Negative reviews by theme)
# ─────────────────────────────────────────
negative_df = df[df['sentiment_label'] == 'negative']
pain_points = negative_df.groupby(
    ['bank', 'identified_theme']
).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(12, 6))
pain_points.plot(kind='bar', ax=ax, colormap='Reds')
ax.set_title('Pain Points — Negative Reviews by Theme per Bank',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Bank')
ax.set_ylabel('Number of Negative Reviews')
ax.tick_params(axis='x', labelrotation=15)
plt.tight_layout()
plt.savefig('data/plots/plot6_pain_points.png', dpi=150)
plt.close()
print("✅ Plot 6 saved — Pain Points")

# ─────────────────────────────────────────
# PLOT 7: Satisfaction Drivers (Positive reviews by theme)
# ─────────────────────────────────────────
positive_df = df[df['sentiment_label'] == 'positive']
drivers = positive_df.groupby(
    ['bank', 'identified_theme']
).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(12, 6))
drivers.plot(kind='bar', ax=ax, colormap='Greens')
ax.set_title('Satisfaction Drivers — Positive Reviews by Theme per Bank',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Bank')
ax.set_ylabel('Number of Positive Reviews')
ax.tick_params(axis='x', labelrotation=15)
plt.tight_layout()
plt.savefig('data/plots/plot7_satisfaction_drivers.png', dpi=150)
plt.close()
print("✅ Plot 7 saved — Satisfaction Drivers")