import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Callable, Optional
from collections import Counter
from datetime import datetime
from article import Article


class NewsProcessor:
    """
    Class to process and visualize news articles data.
    """

    def to_df(self, articles: List[Article],
              sort_by: Optional[Callable] = None,
              filter_func: Optional[Callable] = None) -> pd.DataFrame:
        """
        Convert list of Article objects to a Pandas DataFrame.

        Args:
            articles: List of Article objects
            sort_by: Optional function taking an Article and returning a sort key
            filter_func: Optional function taking an Article and returning True/False

        Returns:
            Pandas DataFrame with one row per article.
        """
        items = articles or []

        # Apply filtering
        if filter_func is not None:
            items = [a for a in items if filter_func(a)]

        # Apply sorting
        if sort_by is not None:
            items = sorted(items, key=sort_by)

        # Convert to records (explicitly pick the fields we care about)
        records = [{
            "url": a.url,
            "source": a.source,
            "author": a.author,
            "title": a.title,
            "description": a.description,
            "publishedAt": a.publishedAt,
            "content": a.content,
        } for a in items]

        cols = ["url", "source", "author", "title", "description", "publishedAt", "content"]
        return pd.DataFrame.from_records(records, columns=cols)

    def plot_word_popularity(self, articles: List[Article], search_term: str):
        """
        Plot the number of articles whose titles contain `search_term` on each day.

        Args:
            articles: List of Article objects
            search_term: The term to search for in titles (case-insensitive)
        """
        term = (search_term or "").strip()
        if not term:
            print("No search term provided.")
            return

        # Count presence (>=1 occurrence) per day
        per_day = Counter()
        all_days = set()

        for a in articles or []:
            day = self._extract_date_from_published(getattr(a, "publishedAt", None))
            if not day:
                continue
            all_days.add(day)
            title = getattr(a, "title", "") or ""
            if self._count_word_in_title(title, term) > 0:
                per_day[day] += 1

        if not all_days:
            print("No dated articles to plot.")
            return

        # Build a continuous date range from min to max day, filling missing days with 0
        from datetime import timedelta  # local import to avoid changing module imports
        day_objs = sorted(datetime.strptime(d, "%Y-%m-%d").date() for d in all_days)
        start, end = day_objs[0], day_objs[-1]

        xs = []
        ys = []
        cur = start
        while cur <= end:
            d_str = cur.strftime("%Y-%m-%d")
            xs.append(cur)
            ys.append(per_day.get(d_str, 0))
            cur += timedelta(days=1)

        # Plot (single plot, no explicit colors/styles)
        plt.figure()
        plt.plot(xs, ys, marker="o")
        plt.xlabel("Date")
        plt.ylabel(f'Articles with "{term}" in title')
        plt.title(f'"{term}" popularity in titles over time')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def _extract_date_from_published(self, published_at: Optional[str]) -> Optional[str]:
        """
        Extract YYYY-MM-DD from an ISO 8601 timestamp string like '2024-10-21T12:34:56Z'.

        Returns:
            Date string (YYYY-MM-DD) or None if parsing fails.
        """
        if not published_at:
            return None

        s = str(published_at).strip()
        try:
            # Handle 'Z' UTC suffix
            if s.endswith("Z"):
                s = s[:-1] + "+00:00"
            dt = datetime.fromisoformat(s)
            return dt.date().isoformat()
        except Exception:
            # Fallback: try taking the first 10 chars if they look like a date
            try:
                return datetime.strptime(s[:10], "%Y-%m-%d").date().isoformat()
            except Exception:
                return None

    def _count_word_in_title(self, title: str, search_term: str) -> int:
        """
        Count occurrences of `search_term` in `title` (case-insensitive, substring match).

        Args:
            title: Article title
            search_term: Term to search for

        Returns:
            Integer count of occurrences.
        """
        if not title or not search_term:
            return 0
        return title.lower().count(search_term.lower())
