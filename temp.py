import copy
import json
import random

a = {
  "model": "jobs.joblisting",
  "pk": 1,
  "fields": {
    "title": "Frond end developer",
    "job_location": "Đà Nẵng, Việt Nam",
    "employment_status": "Full Time",
    "application_deadline": "2020-12-29T00:00:00Z",
    "gender": "Female",
    "responsibilities": "Trách nhiệm",
    "experience": "làm được là được",
    "Salary": "250$",
  }
}

luu = []
location = ["Đà Nẵng, Việt Nam", "TP.HCM, Việt Nam", "Hà Nội, Việt Nam", "Bình Dương, Việt Nam"]
title = ["Frond end developer", "Back end developer", "Designer developer", "Network Engineering", "Mobile Developer"]
employment_status = ['Part Time', 'Full Time','Freelancer']
gender = ['Male', 'Female','Any']

for i in range(100):
    a["model"] = "jobs.joblisting"
    a["pk"] = i+1
    for _ in range(4):
        a["fields"]["title"] = title[random.randint(0,4)]
        a["fields"]["job_location"] = location[random.randint(0,3)]
        a["fields"]["employment_status"] = employment_status[random.randint(0,2)]
        a["fields"]["gender"] = gender[random.randint(0,2)]
        a["fields"]["Salary"] = str(random.randint(100,1000)) + "$"
    luu.append(copy.deepcopy(a))


with open('data2.json', 'w') as outfile:
    json.dump(luu, outfile)