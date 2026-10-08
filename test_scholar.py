from search.scholar import get_research_signal


result = get_research_signal(
    "graphene water purification"
)


print("\nResearch Signal")
print("------------------------")

print("Papers found:", result["papers_found"])
print("Highly cited papers:", result["highly_cited_papers"])

print("\nTop papers:")

for paper in result["papers"][:5]:
    print("-", paper.get("title"))