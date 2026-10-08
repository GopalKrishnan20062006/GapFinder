from search.client import SerpApiClient


client = SerpApiClient()


def google_search(query):
    """
    Search Google using SerpApi.
    """

    cache_key = "google_" + query.lower().replace(" ", "_")

    params = {
        "engine": "google",
        "q": query,
    }

    return client.search(params, cache_key)