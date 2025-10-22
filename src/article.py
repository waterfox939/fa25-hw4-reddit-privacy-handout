class Article:
    """
    Class to store details of a news article from the News API.

    Attributes:
        url: The URL to the article
        source: The source of the article (string; dicts normalized to .get("name") or .get("id"))
        author: The author of the article
        title: The title of the article
        description: A brief description of the article
        published_at: The date/time the article was published (ISO string)
        content: The content of the article
    """

    def __init__(self, url=None, source=None, author=None, title=None,
                 description=None, publishedAt=None, published_at=None, content=None):
        # Normalize source: NewsAPI often returns a dict {"id": ..., "name": ...}
        if isinstance(source, dict):
            source = source.get("name") or source.get("id")

        # Prefer snake_case published_at; fall back to camelCase arg
        pub = published_at if published_at is not None else publishedAt

        self.url = url
        self.source = source
        self.author = author
        self.title = title
        self.description = description
        self.published_at = pub
        self.content = content

    # Backward-compat: camelCase alias so code/tests using publishedAt don't break
    @property
    def publishedAt(self):
        return self.published_at

    @publishedAt.setter
    def publishedAt(self, value):
        self.published_at = value

    def __str__(self):
        """Concise human-readable string."""
        title = self.title or "(no title)"
        src = self.source or "Unknown source"
        when = f" [{self.published_at}]" if self.published_at else ""
        return f"{title} — {src}{when}"

    def __repr__(self):
        """Detailed representation for debugging/tests."""
        return (
            "Article("
            f"url={self.url!r}, "
            f"source={self.source!r}, "
            f"author={self.author!r}, "
            f"title={self.title!r}, "
            f"description={self.description!r}, "
            f"published_at={self.published_at!r}, "
            f"content={self.content!r}"
            ")"
        )
