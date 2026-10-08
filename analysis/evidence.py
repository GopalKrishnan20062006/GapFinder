from search.scholar import get_research_signal
from search.patents import get_patent_signal
from search.shopping import get_market_signal
from search.trends import get_demand_signal
from search.news import get_industry_signal
from search.jobs import get_jobs_signal

from search.query_strategy import build_queries, parse_topic


def safe_search(function, query, default):
    try:
        return function(query)
    except Exception as e:
        print(f"[WARNING] Search failed: {e}")
        return default


def collect_evidence(query):
    parsed_topic = parse_topic(query)
    queries = build_queries(query)

    print("\nCollecting evidence...")

    research = safe_search(
        get_research_signal,
        queries["scholar"],
        {
            "query": queries["scholar"],
            "papers_found": 0,
            "highly_cited_papers": 0,
            "papers": [],
        },
    )

    patents = safe_search(
        get_patent_signal,
        queries["patents"],
        {
            "query": queries["patents"],
            "patents_found": 0,
            "patents": [],
        },
    )

    market = safe_search(
        get_market_signal,
        queries["shopping"],
        {
            "query": queries["shopping"],
            "products_found": 0,
            "products": [],
        },
    )

    demand = safe_search(
        get_demand_signal,
        queries["trends"],
        {
            "query": queries["trends"],
            "data_points": 0,
            "average_interest": 0,
            "recent_interest": 0,
            "trend": "unknown",
        },
    )

    industry = safe_search(
        get_industry_signal,
        queries["news"],
        {
            "query": queries["news"],
            "articles_found": 0,
            "unique_sources": 0,
            "articles": [],
        },
    )

    jobs = safe_search(
        get_jobs_signal,
        queries["jobs"],
        {
            "query": queries["jobs"],
            "jobs_found": 0,
            "unique_companies": 0,
            "jobs": [],
        },
    )

    return {
        "query": query,
        "topic": parsed_topic,
        "queries": queries,
        "research": research,
        "patents": patents,
        "market": market,
        "demand": demand,
        "industry": industry,
        "jobs": jobs,
    }