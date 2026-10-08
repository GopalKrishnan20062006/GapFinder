from search.news import get_industry_signal


result = get_industry_signal(
    "graphene water purification"
)


print("\nIndustry Signal")
print("------------------------")

print("Articles found:", result["articles_found"])
print("Unique sources:", result["unique_sources"])

print("\nTop articles:")

for article in result["articles"][:5]:
    title = article.get("title")
    source = article.get("source")

    print(f"- {title}")
    print(f"  Source: {source}")