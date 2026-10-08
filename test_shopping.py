from search.shopping import get_market_signal


result = get_market_signal(
    "graphene water purification"
)


print("\nMarket Signal")
print("------------------------")

print("Products found:", result["products_found"])

print("\nProducts:")

for product in result["products"][:5]:
    title = product.get("title")
    price = product.get("price")
    source = product.get("source")

    print(f"- {title}")
    print(f"  Price: {price}")
    print(f"  Seller: {source}")