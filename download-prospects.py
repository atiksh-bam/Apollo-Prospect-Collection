## presets ###########################
import requests
from requests.structures import CaseInsensitiveDict
from csv import writer

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
######################################

# open file to write data in(should be csv)
file = open('file-name.csv', 'a', newline='')

# which pages to get data from
pageStart = 1
pageEnd = 101

# configuraations and filters for the request
# you can easily change them according to you
data = """{
  "api_key": "<YOUR_API_KEY>",
  "person_titles": ["trader", "portfolio manager", "financial analyst", "asset manager", "head trader", "data scientist", "data engineer", "data analyst", "data manager", "data specialist", "credit analyst", "credit manager", "credit officer", "credit", "capital markets"],
  "person_locations": ["New York, US", "New Jersey, US", "Massachusetts, US", "California, US", "Connecticut, US"],
  "organization_num_employees_ranges": ["501,1000"],
  "organization_industry_tag_ids": ["5567ce237369644ee5490000", "5567e1ab7369641f6d660100", "5567cdd67369643e64020000"],
  "page": %d
}"""

# make sure to check out the apollo api request limit to avoid issues
people = []
wr = writer(file)

## loop ##############################
for i in range(pageStart,pageEnd):
	result = requests.post("https://api.apollo.io/v1/mixed_people/search", headers=headers, data=data%(i))
	if(result.status_code != 200):
		print("Error")
		continue
	ppl = result.json()["people"]
	#avoiding duplicates or useless prospects
	[people.append([p["id"], p["name"], p["title"], p["headline"], p["organization"]["name"], p["linkedin_url"]]) for p in ppl if (([p["id"], p["name"], p["title"], p["headline"], p["organization"]["name"], p["linkedin_url"]] not in people) and (p["email"] != None))]
	# updates to keep track of progress
	# in case of error check the last page it added data from
	print("Added data from page %d"%(i))
######################################
for p in people:
	wr.writerow(p)