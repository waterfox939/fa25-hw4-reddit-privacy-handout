import unittest
import importlib
from unittest.mock import patch, MagicMock
from src.article import Article


# Change this to the actual filename (module) of your example usage script
USAGE_MODULE = "main"  # e.g., "example_usage" if your file is example_usage.py


class TestExampleMain(unittest.TestCase):
    def test_main_runs_with_mocks(self):
        # Build a tiny fake article list
        fake_articles = [
            Article(
                url="u", source="S", author="A", title="T",
                description="D", published_at="2023-10-01T00:00:00Z", content="C"
            )
        ]

        # Dummy classes to patch into the usage module
        class DummySearchNews:
            def __init__(self, *args, **kwargs):
                self.calls = []

            def get_top_headlines(self, *args, **kwargs):
                self.calls.append(("get_top_headlines", args, kwargs))
                return fake_articles

            def get_everything(self, *args, **kwargs):
                self.calls.append(("get_everything", args, kwargs))
                return fake_articles

        class DummyNewsProcessor:
            def to_df(self, articles, **kwargs):
                # Return a minimal DataFrame-like object or a dict; the code only prints
                import pandas as pd
                return pd.DataFrame([{
                    "url": a.url, "source": a.source, "author": a.author,
                    "title": a.title, "description": a.description,
                    "published_at": a.published_at, "content": a.content
                } for a in articles])

            def plot_word_popularity(self, articles, term):
                # No-op for test
                return None

        # Import the module, then patch the names it imported
        mod = importlib.import_module(USAGE_MODULE)

        with patch.object(mod, "SearchNews", DummySearchNews), \
             patch.object(mod, "NewsProcessor", DummyNewsProcessor):
            # Should run without raising
            mod.main()


if __name__ == "__main__":
    unittest.main()
