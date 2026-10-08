
def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(value, maximum))


def detect_gap(signals, trend_momentum=0):
    """
    Detect commercialization gaps using
    technology strength, supply, and signal convergence.
    """

    research = signals["research"]
    patents = signals["patents"]
    market = signals["market"]
    demand = signals["demand"]
    industry = signals["industry"]
    jobs = signals["jobs"]

    supporting_signals = [
        research,
        patents,
        demand,
        industry,
        jobs,
    ]

    technology_strength = (
        research * 0.25
        + patents * 0.15
        + demand * 0.25
        + industry * 0.20
        + jobs * 0.15
    )

    supply_strength = market

    strong_signals = sum(
        score >= 60
        for score in supporting_signals
    )

    convergence = (
        strong_signals
        / len(supporting_signals)
        * 100
    )

    emerging_gap_bonus = 0

    if trend_momentum >= 70 and market < 40:
        emerging_gap_bonus = 15

    raw_gap = (
        technology_strength
        - supply_strength
    )

    gap_score = (
        raw_gap * 0.65
        + convergence * 0.25
        + emerging_gap_bonus
    )

    gap_score = clamp(gap_score)

    if gap_score >= 70:
        category = "Strong commercialization gap"

    elif gap_score >= 50:
        category = "Moderate commercialization gap"

    elif gap_score >= 30:
        category = "Weak commercialization gap"

    elif gap_score >= 0:
        category = "Limited commercialization gap"

    else:
        category = "Market appears relatively mature"

    return {
        "technology_strength": round(
            technology_strength,
            2,
        ),
        "supply_strength": round(
            supply_strength,
            2,
        ),
        "convergence": round(
            convergence,
            2,
        ),
        "strong_signals": strong_signals,
        "gap_score": round(
            gap_score,
            2,
        ),
        "category": category,
        "trend_momentum": trend_momentum,
        "emerging_gap_bonus": emerging_gap_bonus,
    }


def calculate_opportunity_score(
    signals,
    gap,
):
    """
    Calculate overall commercialization opportunity.
    """

    demand = signals["demand"]
    research = signals["research"]
    industry = signals["industry"]
    jobs = signals["jobs"]

    gap_score = gap["gap_score"]
    convergence = gap["convergence"]

    score = (
        demand * 0.20
        + research * 0.10
        + industry * 0.10
        + jobs * 0.10
        + gap_score * 0.35
        + convergence * 0.15
    )

    if demand < 20:
        score *= 0.6

    return round(
        clamp(score),
        2,
    )


def classify_opportunity(score):

    if score >= 75:
        return "High opportunity"

    if score >= 55:
        return "Promising opportunity"

    if score >= 35:
        return "Moderate opportunity"

    return "Low opportunity"