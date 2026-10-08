from search.client import SerpApiClient


client = SerpApiClient()


def trends_search(query):
    """
    Search Google Trends using SerpApi.
    """

    cache_key = "trends_" + query.lower().replace(" ", "_")

    params = {
        "engine": "google_trends",
        "q": query,
        "data_type": "TIMESERIES",
    }

    return client.search(params, cache_key)


def get_demand_signal(query):
    """
    Extract basic demand information from Google Trends.
    """

    results = trends_search(query)

    interest_data = results.get("interest_over_time", {})

    timeline = interest_data.get("timeline_data", [])

    values = []

    for point in timeline:
        values_list = point.get("values", [])

        if values_list:
            value = values_list[0].get("extracted_value")

            if value is not None:
                values.append(value)

    if not values:
        return {
            "query": query,
            "data_points": 0,
            "average_interest": 0,
            "recent_interest": 0,
            "trend": "unknown",
        }

    average_interest = sum(values) / len(values)

    recent_interest = values[-1]

    # Compare the recent interest with the average.
    if recent_interest > average_interest * 1.2:
        trend = "rising"
    elif recent_interest < average_interest * 0.8:
        trend = "falling"
    else:
        trend = "stable"

    return {
        "query": query,
        "data_points": len(values),
        "average_interest": round(average_interest, 2),
        "recent_interest": recent_interest,
        "trend": trend,
    }