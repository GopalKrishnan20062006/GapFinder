from search.trends import get_demand_signal


result = get_demand_signal(
    "graphene water purification"
)


print("\nDemand Signal")
print("------------------------")

print("Data points:", result["data_points"])
print("Average interest:", result["average_interest"])
print("Recent interest:", result["recent_interest"])
print("Trend:", result["trend"])