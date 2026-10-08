from search.client import SerpApiClient


client = SerpApiClient()


def shopping_search(query):
    """
    Search Google Shopping using SerpApi.
    """

    cache_key = "shopping_" + query.lower().replace(" ", "_")

    params = {
        "engine": "google_shopping",
        "q": query,
    }

    return client.search(params, cache_key)


def get_market_signal(query):
    """
    Search Google Shopping and extract basic
    commercial availability information.
    """

    results = shopping_search(query)

    products = results.get("shopping_results", [])

    return {
        "query": query,
        "products_found": len(products),
        "products": products,
    }