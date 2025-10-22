import unittest
import tempfile
from unittest.mock import patch, MagicMock
from src.search_news import SearchNews
from src.article import Article
import requests


class TestSearchNews(unittest.TestCase):
    def test_initialization_with_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            SearchNews("does_not_exist.txt")

    def test_initialization_reads_key(self):
        with tempfile.NamedTemporaryFile("w+", delete=True) as tf:
            tf.write("FAKEKEY123")
            tf.flush()
            s = SearchNews(tf.name)
            self.assertEqual(s.api_key, "FAKEKEY123")

    @patch("requests.get")
    def test_get_top_headlines_success(self, mock_get):
        # Fake JSON response
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "status": "ok",
                "articles": [
                    {
                        "url": "u1",
                        "source": {"name": "S1"},
                        "author": "A1",
                        "title": "Tech today",
                        "description": "d1",
                        "publishedAt": "2023-10-01T00:00:00Z",
                        "content": "c1",
                    },
                    {
                        "url": "u2",
                        "source": {"name": "S2"},
                        "author": None,
                        "title": "More tech",
                        "description": "d2",
                        "publishedAt": "2023-10-02T00:00:00Z",
                        "content": "c2",
                    },
                ],
            },
        )

        with tempfile.NamedTemporaryFile("w+", delete=True) as tf:
            tf.write("KEY123")
            tf.flush()
            s = SearchNews(tf.name)
            articles = s.get_top_headlines(None, None, "en", "technology", "AI")

        # Returned objects
        self.assertIsInstance(articles, list)
        self.assertTrue(all(isinstance(a, Article) for a in articles))
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].published_at, "2023-10-01T00:00:00Z")

        # Request details
        args, kwargs = mock_get.call_args
        self.assertIn("/v2/top-headlines", args[0])
        headers = kwargs.get("headers", {})
        params = kwargs.get("params", {})
        self.assertEqual(headers.get("X-Api-Key"), "KEY123")
        self.assertEqual(params.get("language"), "en")
        self.assertIn("technology", params.get("q", ""))
        self.assertIn("AI", params.get("q", ""))

    @patch("requests.get")
    def test_get_everything_success(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "status": "ok",
                "articles": [
                    {
                        "url": "u",
                        "source": {"name": "BBC"},
                        "author": "Ann",
                        "title": "Climate change now",
                        "description": "d",
                        "publishedAt": "2025-10-20T05:00:00Z",
                        "content": "c",
                    }
                ],
            },
        )

        with tempfile.NamedTemporaryFile("w+", delete=True) as tf:
            tf.write("KEY999")
            tf.flush()
            s = SearchNews(tf.name)
            date = "2025-10-20"
            domain = "bbc.co.uk"
            lang = "en"
            terms = ("climate", "change")
            articles = s.get_everything(date, domain, lang, *terms)

        self.assertEqual(len(articles), 1)
        a = articles[0]
        self.assertEqual(a.source, "BBC")
        self.assertEqual(a.published_at, "2025-10-20T05:00:00Z")

        args, kwargs = mock_get.call_args
        self.assertIn("/v2/everything", args[0])
        headers = kwargs.get("headers", {})
        params = kwargs.get("params", {})
        self.assertEqual(headers.get("X-Api-Key"), "KEY999")
        self.assertEqual(params.get("domains"), domain)
        self.assertEqual(params.get("language"), lang)
        self.assertEqual(params.get("from"), date)
        self.assertEqual(params.get("to"), date)
        self.assertIn("climate", params.get("q", ""))
        self.assertIn("change", params.get("q", ""))

    @patch("requests.get")
    def test_newsapi_error_raises(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"status": "error", "code": "apiKeyInvalid", "message": "Invalid key"},
        )
        with tempfile.NamedTemporaryFile("w+", delete=True) as tf:
            tf.write("BAD")
            tf.flush()
            s = SearchNews(tf.name)
            with self.assertRaises(RuntimeError):
                s.get_top_headlines(None, None, "en", "x")

    @patch("requests.get", side_effect=requests.RequestException("boom"))
    def test_http_exception_wrapped(self, mock_get):
        with tempfile.NamedTemporaryFile("w+", delete=True) as tf:
            tf.write("K")
            tf.flush()
            s = SearchNews(tf.name)
            with self.assertRaises(RuntimeError):
                s.get_everything("2023-10-01", "example.com", "en", "q")


if __name__ == "__main__":
    unittest.main()
