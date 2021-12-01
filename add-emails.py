## presets ###########################
import requests
from requests.structures import CaseInsensitiveDict
import csv
from time import sleep

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
######################################

#this will be the fields to be filled for each prospect we collect
data = """{
  "api_key": "<YOUR_API_KEY>",
  "id": "%s",
  "name": "%s",
  "organization_name": "%s"
}"""

# open file to read data from(should be csv)
file = open('file_name.csv','r', newline="")
people = list(csv.reader(file))
file.close()
# open file to write data to(should be csv) {can be same as file being read}
wr = csv.writer(open('file_name.csv','a', newline=""))
# 0-770
for n in range(681,770):
  row = people[n]
  # making request
  email = requests.post("https://api.apollo.io/v1/people/match", headers=headers, data=data%(row[0], row[1], row[4]))
  # error handling
  if(email.status_code != 200):
    print("Error in line %d"%(n))
    continue
  if(email.json()["person"]["email"] == None):
    continue
  # printing stuff to keep track
  print(email.json()["person"]["email"])
  # updating the prospect list
  # the user id is excluded as we don't need that anymore
  wr.writerow(row[1:] + [email.json()["person"]["email"]])
  # this is only meant to avoid problems with the request limit
  sleep(1)