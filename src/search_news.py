class SearchNews:
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
            # Required by the test: raise FileNotFoundError for bad path
            raise FileNotFoundError(
                f"API key file not found: {api_key_file}"
            ) from e

        if not key:
            # Empty file should be an error too
            raise ValueError(f"API key file '{api_key_file}' is empty.")

        self.api_key = key
