from search.client import SerpApiClient


client = SerpApiClient()


def patent_search(query):
    """
    Search Google Patents using SerpApi.
    """

    cache_key = "patents_" + query.lower().replace(" ", "_")

    params = {
        "engine": "google_patents",
        "q": query,
    }

    return client.search(params, cache_key)


def get_patent_signal(query):
    """
    Search Google Patents and extract basic
    patent activity information.
    """

    results = patent_search(query)

    patents = results.get("organic_results", [])

    return {
        "query": query,
        "patents_found": len(patents),
        "patents": patents,
    }