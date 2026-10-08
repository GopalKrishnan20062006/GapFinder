from search.patents import get_patent_signal


result = get_patent_signal(
    "graphene water purification"
)


print("\nPatent Signal")
print("------------------------")

print("Patents found:", result["patents_found"])

print("\nTop patents:")

for patent in result["patents"][:5]:
    print("-", patent.get("title"))