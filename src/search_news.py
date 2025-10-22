import os
import requests
from typing import Optional, List
from article import Article


class SearchNews:
    """
    Class to interact with the News API and retrieve news articles.
    """

    BASE_URL = "https://newsapi.org/v2"

    def __init__(self, api_key_file: str = "api_key.txt"):
        """
        Initialize SearchNews by reading API key from file.

        Args:
            api_key_file: Path to file containing the API key (default: 'api_key.txt')
        """
        try:
            with open(api_key_file, "r", encoding="utf-8") as f:
                key = f.read().strip()
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"API key file not found: {api_key_file}. "
                "Create the file and put your NewsAPI key inside (single line)."
            ) from e

        if not key:
            raise ValueError(f"API key file '{api_key_file}' is empty.")

        self.api_key = key

    def get_top_headlines(
        self,
        date: Optional[str] = None,       # Not used by this endpoint; kept for API-compat
        domain: Optional[str] = None,     # Not supported on /top-headlines; ignored
        language: Optional[str] = None,
        *terms
    ) -> List[Article]:
        """
        Get top headlines from the News API.

        Args:
            date: Optional date filter (YYYY-MM-DD). (Ignored by this endpoint.)
            domain: Optional domain filter (e.g., 'bbc.co.uk'). (Ignored here.)
            language: Optional language filter (e.g., 'en')
            *terms: Variable number of search terms combined into 'q'

        Returns:
            List[Article]
        """
        params: dict = {}
        if language:
            params["language"] = language
        if terms:
            params["q"] = " ".join(t for t in terms if t)

        data = self._make_request("top-headlines", params)
        return self._create_articles_from_response(data)

    def get_everything(
        self,
        date: Optional[str] = None,
        domain: Optional[str] = None,
        language: Optional[str] = None,
        *terms
    ) -> List[Article]:
        """
        Get articles from the /everything endpoint.

        Args:
            date: Optional date filter (YYYY-MM-DD) – applied to both 'from' and 'to'
            domain: Optional domain filter (e.g., 'bbc.co.uk')
            language: Optional language filter (e.g., 'en')
            *terms: Variable number of search terms combined into 'q'

        Returns:
            List[Article]
        """
        params: dict = {}
        if language:
            params["language"] = language
        if domain:
            params["domains"] = domain
        if terms:
            params["q"] = " ".join(t for t in terms if t)
        if date:
            # Narrow to a single day window
            params["from"] = date
            params["to"] = date
            params["sortBy"] = "publishedAt"

        data = self._make_request("everything", params)
        return self._create_articles_from_response(data)

    def _make_request(self, endpoint: str, params: dict) -> dict:
        """
        Helper to make API requests and handle errors.
        """
        url = f"{self.BASE_URL}/{endpoint}"
        headers = {"X-Api-Key": self.api_key}

        try:
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            raise RuntimeError(f"HTTP error calling NewsAPI: {e}") from e
        except ValueError as e:
            raise RuntimeError("Failed to parse NewsAPI response as JSON.") from e

        # NewsAPI returns {"status":"ok", ...} or {"status":"error", "code":..., "message":...}
        if data.get("status") != "ok":
            code = data.get("code", "unknown_error")
            msg = data.get("message", "Unknown error from NewsAPI.")
            raise RuntimeError(f"NewsAPI error ({code}): {msg}")

        return data

    def _create_articles_from_response(self, response_data: dict) -> List[Article]:
        """
        Build Article objects from the 'articles' array in response.
        """
        articles_raw = response_data.get("articles", []) or []
        articles: List[Article] = []

        for item in articles_raw:
            articles.append(Article(
                url=item.get("url"),
                source=item.get("source"),            # dict with id/name; Article normalizes
                author=item.get("author"),
                title=item.get("title"),
                description=item.get("description"),
                publishedAt=item.get("publishedAt"),
                content=item.get("content"),
            ))

        return articles
