class Article:
    """
    Class to store details of a news article from the News API.

    Attributes:
        url: The URL to the article
        source: The source of the article (name string; dicts are normalized)
        author: The author of the article
        title: The title of the article
        description: A brief description of the article
        publishedAt: The date and time the article was published (string as returned)
        content: The content of the article
    """

    def __init__(self, url=None, source=None, author=None, title=None,
                 description=None, publishedAt=None, content=None):
        """
        Initialize an Article object with the given attributes.
        """
        # Normalize source: NewsAPI often returns {"id": ..., "name": ...}
        if isinstance(source, dict):
            source = source.get("name") or source.get("id")

        self.url = url
        self.source = source
        self.author = author
        self.title = title
        self.description = description
        self.publishedAt = publishedAt
        self.content = content

    def __str__(self):
        """Return a concise human-readable string."""
        src = f"{self.source}" if self.source else "Unknown source"
        ttl = self.title or "(no title)"
        when = f" [{self.publishedAt}]" if self.publishedAt else ""
        return f"{ttl} — {src}{when}"

    def __repr__(self):
        """Return a detailed representation for debugging."""
        return (
            "Article("
            f"url={self.url!r}, "
            f"source={self.source!r}, "
            f"author={self.author!r}, "
            f"title={self.title!r}, "
            f"description={self.description!r}, "
            f"publishedAt={self.publishedAt!r}, "
            f"content={self.content!r}"
            ")"
        )
