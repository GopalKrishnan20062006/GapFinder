from search.client import SerpApiClient


client = SerpApiClient()


def news_search(query):
    """
    Search Google News using SerpApi.
    """

    cache_key = "news_" + query.lower().replace(" ", "_")

    params = {
        "engine": "google_news",
        "q": query,
    }

    return client.search(params, cache_key)


def get_industry_signal(query):
    """
    Extract basic industry activity information
    from Google News.
    """

    results = news_search(query)

    articles = results.get("news_results", [])

    sources = set()

    for article in articles:
        source = article.get("source")

        if source:
            sources.add(source.get("name", "Unknown"))

    return {
        "query": query,
        "articles_found": len(articles),
        "unique_sources": len(sources),
        "articles": articles,
    }