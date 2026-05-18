# tests/test_pipeline.py
# Unit tests for the fintech review analytics pipeline

import pytest
import pandas as pd
import os

# ─────────────────────────────────────────
# Task 1 Tests — Data Collection
# ─────────────────────────────────────────

def test_cleaned_csv_exists():
    """Check that the cleaned CSV file exists."""
    assert os.path.exists('data/bank_reviews_cleaned.csv'), \
        "Cleaned CSV file not found!"

def test_cleaned_csv_has_required_columns():
    """Check that all 5 required columns exist."""
    df = pd.read_csv('data/bank_reviews_cleaned.csv')
    required = {'review', 'rating', 'date', 'bank', 'source'}
    missing = required - set(df.columns)
    assert not missing, f"Missing columns: {missing}"

def test_no_missing_review_text():
    """Check no missing review text."""
    df = pd.read_csv('data/bank_reviews_cleaned.csv')
    assert df['review'].isna().sum() == 0, "Found missing review text!"

def test_no_missing_ratings():
    """Check no missing ratings."""
    df = pd.read_csv('data/bank_reviews_cleaned.csv')
    assert df['rating'].isna().sum() == 0, "Found missing ratings!"

def test_ratings_are_valid():
    """Check all ratings are between 1 and 5."""
    df = pd.read_csv('data/bank_reviews_cleaned.csv')
    assert df['rating'].between(1, 5).all(), \
        "Some ratings are outside 1-5 range!"

def test_three_banks_present():
    """Check all three banks are in the dataset."""
    df = pd.read_csv('data/bank_reviews_cleaned.csv')
    banks = set(df['bank'].unique())
    expected = {'CBE', 'BOA', 'Dashen'}
    assert expected == banks, f"Expected banks {expected}, got {banks}"

def test_date_format_is_correct():
    """Check dates are in YYYY-MM-DD format."""
    df = pd.read_csv('data/bank_reviews_cleaned.csv')
    try:
        pd.to_datetime(df['date'], format='%Y-%m-%d')
    except Exception:
        pytest.fail("Date format is not YYYY-MM-DD!")

def test_source_is_google_play():
    """Check source column is always Google Play."""
    df = pd.read_csv('data/bank_reviews_cleaned.csv')
    assert (df['source'] == 'Google Play').all(), \
        "Source column contains values other than Google Play!"

# ─────────────────────────────────────────
# Task 2 Tests — Sentiment Analysis
# ─────────────────────────────────────────

def test_sentiment_csv_exists():
    """Check sentiment CSV exists."""
    assert os.path.exists('data/bank_reviews_sentiment.csv'), \
        "Sentiment CSV not found!"

def test_sentiment_labels_are_valid():
    """Check sentiment labels are only positive/negative/neutral."""
    df = pd.read_csv('data/bank_reviews_sentiment.csv')
    valid = {'positive', 'negative', 'neutral'}
    invalid = set(df['sentiment_label'].unique()) - valid
    assert not invalid, f"Invalid sentiment labels found: {invalid}"

def test_sentiment_coverage_above_90_percent():
    """Check sentiment is assigned to 90%+ of reviews."""
    df = pd.read_csv('data/bank_reviews_sentiment.csv')
    coverage = df['sentiment_label'].notna().sum() / len(df) * 100
    assert coverage >= 90, f"Sentiment coverage is {coverage:.1f}%, need 90%+"

def test_sentiment_scores_in_valid_range():
    """Check sentiment scores are between -1 and 1."""
    df = pd.read_csv('data/bank_reviews_sentiment.csv')
    assert df['sentiment_score'].between(-1, 1).all(), \
        "Some sentiment scores are outside -1 to 1 range!"

# ─────────────────────────────────────────
# Task 2 Tests — Thematic Analysis
# ─────────────────────────────────────────

def test_analyzed_csv_exists():
    """Check analyzed CSV exists."""
    assert os.path.exists('data/bank_reviews_analyzed.csv'), \
        "Analyzed CSV not found!"

def test_themes_are_assigned():
    """Check all reviews have a theme assigned."""
    df = pd.read_csv('data/bank_reviews_analyzed.csv')
    assert df['identified_theme'].isna().sum() == 0, \
        "Some reviews have no theme!"

def test_minimum_three_themes_per_bank():
    """Check at least 3 distinct themes per bank."""
    df = pd.read_csv('data/bank_reviews_analyzed.csv')
    for bank in df['bank'].unique():
        themes = df[df['bank'] == bank]['identified_theme'].nunique()
        assert themes >= 3, \
            f"{bank} has only {themes} themes, need at least 3!"

def test_task2_output_has_required_columns():
    """Check task2 final output has all required columns."""
    df = pd.read_csv('data/task2_final_output.csv')
    required = {'review_id', 'review_text', 'sentiment_label',
                'sentiment_score', 'identified_theme'}
    missing = required - set(df.columns)
    assert not missing, f"Missing columns in task2 output: {missing}"

# ─────────────────────────────────────────
# Task 3 Tests — Database
# ─────────────────────────────────────────

def test_schema_sql_exists():
    """Check schema.sql file exists."""
    assert os.path.exists('schema.sql'), \
        "schema.sql file not found!"

def test_tfidf_keywords_csv_exists():
    """Check TF-IDF keywords CSV exists."""
    assert os.path.exists('data/tfidf_keywords.csv'), \
        "TF-IDF keywords CSV not found!"