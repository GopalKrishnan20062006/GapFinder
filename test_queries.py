from search.query_strategy import (
    parse_topic,
    build_queries,
)


topic = "graphene water purification for rural communities"


parsed = parse_topic(topic)

queries = build_queries(topic)


print("\nParsed Topic")
print("=" * 50)

print("Core:", parsed["core"])
print("Context:", parsed["context"])


print("\nGenerated Queries")
print("=" * 50)

for engine, query in queries.items():
    print(f"{engine.capitalize():12} → {query}")