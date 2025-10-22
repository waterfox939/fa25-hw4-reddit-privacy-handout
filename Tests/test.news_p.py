import unittest
from unittest.mock import patch
import pandas as pd
from src.article import Article
from src.news_processor import NewsProcessor


class TestNewsProcessor(unittest.TestCase):
    def setUp(self):
        self.articles = [
            Article(
                url="u1", source="S1", author="A1",
                title="Breaking News: Python is awesome",
                description="d1",
                published_at="2023-10-02T10:00:00Z",
                content="c1",
            ),
            Article(
                url="u2", source="S2", author=None,
                title="AI trends today",
                description="d2",
                published_at="2023-10-01T09:00:00Z",
                content="c2",
            ),
            Article(
                url="u3", source="S3", author="A3",
                title="Something else",
                description="d3",
                published_at=None,
                content="c3",
            ),
        ]
        self.np = NewsProcessor()

    def test_to_df_no_sort_no_filter(self):
        df = self.np.to_df(self.articles)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertListEqual(
            list(df.columns),
            ["url", "source", "author", "title", "description", "published_at", "content"],
        )

    def test_to_df_with_sort_no_filter(self):
        df = self.np.to_df(self.articles, sort_by=lambda a: a.title or "")
        self.assertEqual(df.iloc[0]["title"], "AI trends today")

    def test_to_df_with_filter_no_sort(self):
        df = self.np.to_df(self.articles, filter_func=lambda a: a.author is not None)
        self.assertEqual(len(df), 2)
        self.assertTrue(all(pd.notna(df["author"])))

    def test_to_df_with_sort_and_filter(self):
        df = self.np.to_df(
            self.articles,
            sort_by=lambda a: (a.published_at or ""),
            filter_func=lambda a: a.author is not None,
        )
        self.assertEqual(len(df), 2)
        # first row should be the earlier date
        self.assertEqual(df.iloc[0]["published_at"], "2023-10-02T10:00:00Z")

    @patch("matplotlib.pyplot.show")
    def test_plot_word_popularity_no_crash(self, mock_show):
        # Should not raise; should call plt.show()
        self.np.plot_word_popularity(self.articles, "AI")
        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
