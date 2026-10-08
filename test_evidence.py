from analysis.evidence import collect_evidence


evidence = collect_evidence(
    "graphene water purification"
)


print("\n" + "=" * 50)
print("GAPFINDER EVIDENCE")
print("=" * 50)

print("\nResearch")
print("Papers:", evidence["research"]["papers_found"])

print("\nPatents")
print("Patents:", evidence["patents"]["patents_found"])

print("\nMarket")
print("Products:", evidence["market"]["products_found"])

print("\nDemand")
print("Average interest:", evidence["demand"]["average_interest"])
print("Trend:", evidence["demand"]["trend"])

print("\nIndustry")
print("Articles:", evidence["industry"]["articles_found"])
print("Sources:", evidence["industry"]["unique_sources"])

print("\nJobs")
print("Jobs:", evidence["jobs"]["jobs_found"])
print("Companies:", evidence["jobs"]["unique_companies"])