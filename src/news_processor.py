import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Callable, Optional
from collections import Counter
from datetime import datetime, timedelta
from article import Article


class NewsProcessor:
    """
    Class to process and visualize news articles data.
    """

    def to_df(
        self,
        articles: List[Article],
        sort_by: Optional[Callable] = None,
        filter: Optional[Callable] = None,   # match spec/tests: 'filter', not 'filter_func'
    ) -> pd.DataFrame:
        """
        Convert list of Article objects to a Pandas DataFrame.

        Args:
            articles: List[Article]
            sort_by: Optional function taking an Article -> sort key
            filter: Optional function taking an Article -> bool (keep if True)

        Returns:
            pd.DataFrame with one row per article.
        """
        items = list(articles or [])

        # Apply filtering first
        if filter is not None:
            items = [a for a in items if filter(a)]

        # Then apply sorting
        if sort_by is not None:
            items = sorted(items, key=sort_by)

        # Convert to records; each Article attribute becomes a column
        records = [{
            "url": a.url,
            "source": a.source,
            "author": a.author,
            "title": a.title,
            "description": a.description,
            "published_at": a.published_at,   # using snake_case attribute from your Article
            "content": a.content,
        } for a in items]

        columns = ["url", "source", "author", "title", "description", "published_at", "content"]
        return pd.DataFrame.from_records(records, columns=columns)

    def plot_word_popularity(self, articles: List[Article], search_term: str):
        """
        Plot the frequency (count of articles whose title contains the term) per day.
        """
        term = (search_term or "").strip().lower()
        if not term:
            print("No search term provided.")
            return

        per_day = Counter()
        all_days = set()

        for a in articles or []:
            day = self._extract_date_from_published(getattr(a, "published_at", None))
            if not day:
                continue
            all_days.add(day)
            title = (a.title or "").lower()
            if term in title:             # presence in title (per spec)
                per_day[day] += 1

        if not all_days:
            print("No dated articles to plot.")
            return

        day_objs = sorted(datetime.strptime(d, "%Y-%m-%d").date() for d in all_days)
        start, end = day_objs[0], day_objs[-1]

        xs, ys = [], []
        cur = start
        while cur <= end:
            d_str = cur.strftime("%Y-%m-%d")
            xs.append(cur)
            ys.append(per_day.get(d_str, 0))
            cur += timedelta(days=1)

        plt.figure()
        plt.plot(xs, ys, marker="o")
        plt.xlabel("Date")
        plt.ylabel(f'Articles with "{search_term}" in title')
        plt.title(f'"{search_term}" popularity in titles over time')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def _extract_date_from_published(self, published_at: Optional[str]) -> Optional[str]:
        """
        Extract YYYY-MM-DD from ISO 8601 timestamp (e.g., '2023-10-01T12:00:00Z').
        """
        if not published_at:
            return None
        s = str(published_at).strip()
        try:
            if s.endswith("Z"):
                s = s[:-1] + "+00:00"
            dt = datetime.fromisoformat(s)
            return dt.date().isoformat()
        except Exception:
            try:
                return datetime.strptime(s[:10], "%Y-%m-%d").date().isoformat()
            except Exception:
                return None
