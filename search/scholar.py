from search.client import SerpApiClient


client = SerpApiClient()


def scholar_search(query):
    """
    Search Google Scholar using SerpApi.
    """

    cache_key = "scholar_" + query.lower().replace(" ", "_")

    params = {
        "engine": "google_scholar",
        "q": query,
    }

    return client.search(params, cache_key)


def get_research_signal(query):
    """
    Search Google Scholar and extract basic
    research maturity information.
    """

    results = scholar_search(query)

    papers = results.get("organic_results", [])

    total_papers = len(papers)

    highly_cited = 0

    for paper in papers:
        cited_by = paper.get("inline_links", {}).get("cited_by", {})

        if cited_by:
            citation_count = cited_by.get("total", 0)

            if citation_count >= 100:
                highly_cited += 1

    return {
        "query": query,
        "papers_found": total_papers,
        "highly_cited_papers": highly_cited,
        "papers": papers,
    }