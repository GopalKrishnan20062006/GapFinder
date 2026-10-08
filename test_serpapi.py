import serpapi

from config import SERPAPI_KEY


# Create the SerpApi client
client = serpapi.Client(api_key=SERPAPI_KEY)


# Make ONE test search
results = client.search({
    "engine": "google",
    "q": "graphene water purification",
})


# Print a few basic results
print("\nSerpApi connection successful!\n")

print("Search query:")
print(results.get("search_parameters", {}).get("q"))

print("\nFirst few organic results:")

for result in results.get("organic_results", [])[:3]:
    print(
        f"- {result.get('title')}"
    )