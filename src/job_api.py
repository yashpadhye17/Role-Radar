from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()
apify_api_key = os.getenv("APIFY_API_KEY")
os.environ["APIFY_API_KEY"] = apify_api_key

apify_client = ApifyClient(apify_api_key)

## This function fetches job listings from LinkedIn using Apify's LinkedIn Job Scraper actor.
def fetch_linkedin_jobs(search_query, location="United States",rows=100):
    run_input = {
        "keyword": search_query,
        "location": location,
        "rows": rows,
        "freshness": "SevenDays",
        "expereience": "all",
        "proxy": {
        "useApifyProxy": True,
        "apifyProxyGroups": ["RESIDENTIAL"],
        }
    }
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs
