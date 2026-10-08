from search.jobs import get_jobs_signal


result = get_jobs_signal(
    "graphene water purification"
)


print("\nJobs Signal")
print("------------------------")

print("Jobs found:", result["jobs_found"])
print("Unique companies:", result["unique_companies"])

print("\nTop jobs:")

for job in result["jobs"][:5]:
    title = job.get("title")
    company = job.get("company_name")
    location = job.get("location")

    print(f"- {title}")
    print(f"  Company: {company}")
    print(f"  Location: {location}")