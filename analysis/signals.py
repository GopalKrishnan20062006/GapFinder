def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(value, maximum))


def score_research(research):
    papers = research.get("papers_found", 0)
    highly_cited = research.get("highly_cited_papers", 0)

    return clamp(
        papers * 5 + highly_cited * 15
    )


def score_patents(patents):
    patent_count = patents.get("patents_found", 0)

    return clamp(
        patent_count * 8
    )


def score_market(market):
    products = market.get("products_found", 0)

    return clamp(
        products * 10
    )


def score_demand(demand):
    return clamp(
        demand.get("average_interest", 0)
    )


def score_industry(industry):
    articles = industry.get("articles_found", 0)
    sources = industry.get("unique_sources", 0)

    return clamp(
        articles * 5 + sources * 5
    )


def score_jobs(jobs):
    job_count = jobs.get("jobs_found", 0)
    company_count = jobs.get("unique_companies", 0)

    return clamp(
        job_count * 5 + company_count * 5
    )


def calculate_signals(evidence):

    return {
        "research": score_research(
            evidence["research"]
        ),

        "patents": score_patents(
            evidence["patents"]
        ),

        "market": score_market(
            evidence["market"]
        ),

        "demand": score_demand(
            evidence["demand"]
        ),

        "industry": score_industry(
            evidence["industry"]
        ),

        "jobs": score_jobs(
            evidence["jobs"]
        ),
    }


def calculate_confidence(evidence):
    """
    Estimate confidence from evidence coverage
    and source diversity.
    """

    research = evidence["research"]
    patents = evidence["patents"]
    market = evidence["market"]
    industry = evidence["industry"]
    jobs = evidence["jobs"]

    components = []

    # Research confidence
    papers = research.get("papers_found", 0)
    components.append(
        min(papers / 10, 1) * 100
    )

    # Patent confidence
    patents_found = patents.get("patents_found", 0)
    components.append(
        min(patents_found / 10, 1) * 100
    )

    # Market confidence
    products = market.get("products_found", 0)
    components.append(
        min(products / 10, 1) * 100
    )

    # Industry confidence
    articles = industry.get("articles_found", 0)
    sources = industry.get("unique_sources", 0)

    industry_confidence = (
        min(articles / 10, 1) * 50
        + min(sources / 5, 1) * 50
    )

    components.append(industry_confidence)

    # Hiring confidence
    jobs_found = jobs.get("jobs_found", 0)
    companies = jobs.get("unique_companies", 0)

    jobs_confidence = (
        min(jobs_found / 10, 1) * 50
        + min(companies / 5, 1) * 50
    )

    components.append(jobs_confidence)

    return round(
        sum(components) / len(components),
        2,
    )
def calculate_trend_momentum(demand):
    """
    Estimate whether search interest is accelerating.
    """

    trend = demand.get("trend", "unknown")

    if trend == "rising":
        return 80

    if trend == "stable":
        return 50

    if trend == "falling":
        return 20

    return 0