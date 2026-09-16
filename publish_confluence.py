import os
import requests

print("Python script is running")

CONFLUENCE_URL = os.environ["CONFLUENCE_URL"]
CONFLUENCE_TOKEN = os.environ["CONFLUENCE_TOKEN"]
CONFLUENCE_PAGE_ID = os.environ["CONFLUENCE_PAGE_ID"]

#with open("wiki/Home.md", "r") as file: means: open the Home.md file inside the wiki folder in read mode. "r" means read.

with open("wiki/Home.md", "r") as file:  
  content = file.read()                 #reads everything inside Home.md and stores it in content.

headers = {
  "Authorization": f"Bearer {CONFLUENCE_TOKEN}",
  "Accept": "application/json"
}

url = f"{CONFLUENCE_URL}/rest/api/content/{CONFLUENCE_PAGE_ID}?expand=version"

response = requests.get(url, headers=headers)

print("Confluence response status:", response.status_code)

if response.status_code == 200:
  page = response.json()
  print("COnnected to COnfluence successfully")
  print("Page title:", page["title"])
  print("Current version:", page["version"]["number"])

else:
    print("Failed to retrive the COnfluence page")
    print(response.text)
        

print("Wiki Home page content:")
print(content)
