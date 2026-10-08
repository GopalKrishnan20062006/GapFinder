def evidence_strength(count, thresholds=(3, 7)):
    if count >= thresholds[1]:
        return "strong"
    if count >= thresholds[0]:
        return "moderate"
    return "limited"


def build_report(query, evidence, signals, gap, confidence):
    findings = []

    research = signals["research"]
    patents = signals["patents"]
    market = signals["market"]
    demand = signals["demand"]
    industry = signals["industry"]
    jobs = signals["jobs"]

    research_count = evidence["research"]["papers_found"]
    patent_count = evidence["patents"]["patents_found"]
    product_count = evidence["market"]["products_found"]
    news_count = evidence["industry"]["articles_found"]
    company_count = evidence["jobs"]["unique_companies"]

    findings.append(
        f"Research evidence is {evidence_strength(research_count)} "
        f"with {research_count} papers identified."
    )

    findings.append(
        f"Patent activity is {evidence_strength(patent_count)} "
        f"with {patent_count} relevant patents identified."
    )

    findings.append(
        f"Commercial supply is {evidence_strength(product_count)} "
        f"with {product_count} products identified."
    )

    findings.append(
        f"Industry activity includes {news_count} news articles "
        f"across {evidence['industry']['unique_sources']} sources."
    )

    findings.append(
        f"Hiring evidence includes {company_count} companies "
        f"and {evidence['jobs']['jobs_found']} job listings."
    )

    if demand >= 60:
        findings.append("Search demand is strong.")
    elif demand >= 30:
        findings.append("Search demand is moderate.")
    else:
        findings.append("Search demand is weak.")

    if gap["trend_momentum"] >= 70 and market < 40:
        findings.append(
            "An emerging gap is detected because demand is rising while "
            "commercial supply remains limited."
        )

    if gap["gap_score"] >= 70:
        conclusion = (
            f"{query} shows a strong commercialization gap. "
            "Multiple independent signals indicate meaningful technology, "
            "demand, and industry activity while commercial supply remains weak."
        )
    elif gap["gap_score"] >= 50:
        conclusion = (
            f"{query} shows a moderate commercialization gap. "
            "There are encouraging signals, but the evidence is not yet "
            "strong enough to indicate a clearly underserved market."
        )
    elif gap["gap_score"] >= 30:
        conclusion = (
            f"{query} shows a weak commercialization gap. "
            "Some opportunity exists, but the evidence suggests limited "
            "demand or significant existing supply."
        )
    else:
        conclusion = (
            f"{query} does not currently show a significant commercialization gap. "
            "The available evidence suggests a relatively mature market or "
            "limited commercial opportunity."
        )

    return {
        "query": query,
        "findings": findings,
        "conclusion": conclusion,
        "signals": signals,
        "gap": gap,
        "confidence": confidence,
        "evidence": {
            "research_papers": research_count,
            "patents": patent_count,
            "products": product_count,
            "trend": evidence["demand"]["trend"],
            "news_articles": news_count,
            "companies_hiring": company_count,
        },
    }