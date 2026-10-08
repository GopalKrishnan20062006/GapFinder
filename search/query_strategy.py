import re


def parse_topic(topic):
    """
    Extract the core topic and optional context.
    """

    topic = topic.strip()

    match = re.match(
        r"(.+?)\s+(?:for|in|within|targeting)\s+(.+)",
        topic,
        re.IGNORECASE,
    )

    if match:
        core = match.group(1).strip()
        context = match.group(2).strip()
    else:
        core = topic
        context = ""

    return {
        "core": core,
        "context": context,
    }


def build_queries(topic):
    """
    Build engine-specific queries.
    """

    parsed = parse_topic(topic)

    core = parsed["core"]
    context = parsed["context"]

    context_part = f" {context}" if context else ""

    return {
        "scholar": f"{core}{context_part}",

        "patents": f"{core} technology",

        "shopping": f"{core} filter product",

        "trends": core,

        "news": f"{core} industry",

        "jobs": f"{core} engineer",
    }