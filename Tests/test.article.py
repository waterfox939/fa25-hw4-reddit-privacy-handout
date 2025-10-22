import unittest
from src.article import Article


class TestArticle(unittest.TestCase):
    def setUp(self):
        self.sample = {
            "url": "https://example.com/article",
            "source": "Example Source",
            "author": "John Doe",
            "title": "Example Title",
            "description": "This is an example description.",
            "published_at": "2023-10-01T12:00:00Z",
            "content": "This is the content of the example article.",
        }

    def test_attributes_set(self):
        a = Article(**self.sample)
        self.assertEqual(a.url, self.sample["url"])
        self.assertEqual(a.source, self.sample["source"])
        self.assertEqual(a.author, self.sample["author"])
        self.assertEqual(a.title, self.sample["title"])
        self.assertEqual(a.description, self.sample["description"])
        self.assertEqual(a.published_at, self.sample["published_at"])
        self.assertEqual(a.content, self.sample["content"])

    def test_source_normalization_from_dict(self):
        a = Article(
            url="u",
            source={"id": "ex", "name": "Example Source"},
            author=None,
            title=None,
            description=None,
            published_at=None,
            content=None,
        )
        self.assertEqual(a.source, "Example Source")  # prefers name over id

    def test_str_format(self):
        a = Article(**self.sample)
        expected = "Example Title by John Doe from Example Source on 2023-10-01T12:00:00Z"
        self.assertEqual(str(a), expected)

    def test_repr_format(self):
        a = Article(**self.sample)
        expected = (
            "Article(title='Example Title', author='John Doe', "
            "source='Example Source', publishedAt='2023-10-01T12:00:00Z')"
        )
        self.assertEqual(repr(a), expected)


if __name__ == "__main__":
    unittest.main()
