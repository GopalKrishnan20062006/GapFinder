import json
from pathlib import Path

import serpapi

from config import SERPAPI_KEY, MAX_SEARCHES


CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

USAGE_FILE = Path("data/search_usage.json")


class SerpApiClient:

    def __init__(self):
        self.client = serpapi.Client(api_key=SERPAPI_KEY)

    def _get_cache_path(self, cache_key):
        return CACHE_DIR / f"{cache_key}.json"

    def _load_usage(self):
        if not USAGE_FILE.exists():
            return {
                "searches_used": 0
            }

        with open(USAGE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_usage(self, usage):
        with open(USAGE_FILE, "w", encoding="utf-8") as file:
            json.dump(usage, file, indent=2)

    def searches_used(self):
        return self._load_usage()["searches_used"]

    def searches_remaining(self):
        return max(
            0,
            MAX_SEARCHES - self.searches_used()
        )

    def search(self, params, cache_key):

        cache_path = self._get_cache_path(cache_key)

        if cache_path.exists():
            print(f"[CACHE] Using saved result: {cache_key}")

            try:
                with open(cache_path, "r", encoding="utf-8") as file:
                 return json.load(file)
            except json.JSONDecodeError:
                print("[CACHE] Invalid cache. Running API request again.")

        if self.searches_remaining() <= 0:
            raise RuntimeError("SerpApi search budget exhausted.")

        print(f"[API] Running SerpApi search: {cache_key}")

        results = self.client.search(params)
        results = results.as_dict()

        usage = self._load_usage()
        usage["searches_used"] += 1
        self._save_usage(usage)

        with open(cache_path, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=2, ensure_ascii=False)

        return results