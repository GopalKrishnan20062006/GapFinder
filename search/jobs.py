from search.client import SerpApiClient


client = SerpApiClient()


def jobs_search(query):
    """
    Search Google Jobs using SerpApi.
    """

    cache_key = "jobs_" + query.lower().replace(" ", "_")

    params = {
        "engine": "google_jobs",
        "q": query,
    }

    return client.search(params, cache_key)


def get_jobs_signal(query):
    """
    Extract basic hiring activity information.
    """

    results = jobs_search(query)

    jobs = results.get("jobs_results", [])

    companies = set()

    for job in jobs:
        company = job.get("company_name")

        if company:
            companies.add(company)

    return {
        "query": query,
        "jobs_found": len(jobs),
        "unique_companies": len(companies),
        "jobs": jobs,
    }