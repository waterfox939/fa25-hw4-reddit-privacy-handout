"""
Example usage of the News API classes.

Before running this code:
1. Get your API key from https://newsapi.org/register
2. Store it in 'api_key.txt' (do NOT push the key to GitHub).
"""

from search_news import SearchNews
from news_processor import NewsProcessor
from datetime import datetime, timedelta


def main():
    # Initialize helpers
    searcher = SearchNews()      # reads key from 'api_key.txt'
    processor = NewsProcessor()

    # Example 1: Get top headlines (English) for term "technology"
    # Signature: get_top_headlines(date=None, domain=None, language=None, *terms)
    print("Getting top headlines...")
    headlines = searcher.get_top_headlines(None, None, "en", "technology")
    print(f"Found {len(headlines)} headlines")

    # Example 2: Convert to DataFrame
    print("\nConverting to DataFrame...")
    df = processor.to_df(headlines)
    print(df.head())

    # Example 3: Filter articles (only articles with authors)
    print("\nFiltering articles with authors...")
    df_with_authors = processor.to_df(
        headlines,
        filter=lambda article: bool(article.author)
    )
    print(f"Articles with authors: {len(df_with_authors)}")

    # Example 4: Sort by publication date (ISO 8601 sorts lexicographically OK)
    print("\nSorting by publication date...")
    df_sorted = processor.to_df(
        headlines,
        sort_by=lambda article: article.publishedAt or ""
    )
    print("Sorted DataFrame created")
    # print(df_sorted.head())

    # Example 5: Plot word popularity
    print("\nPlotting word popularity...")
    processor.plot_word_popularity(headlines, "AI")

    # Example 6: Search everything for a specific term
    print("\nSearching everything for 'climate change'...")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    climate_articles = searcher.get_everything(
        yesterday, None, "en", "climate change"
    )
    print(f"Found {len(climate_articles)} articles about climate change")


if __name__ == "__main__":
    main()
