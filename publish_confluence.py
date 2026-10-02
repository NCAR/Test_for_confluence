# load all libraries


import os              # os gets GitHub secret values
import requests        # requests talk to Confluence REST API
import markdown        # markdown converts GitHub Markdown into HTML
from pathlib import Path

# Getting values from GitHub Secrets

confluence_url = os.environ["CONFLUENCE_URL"].rstrip("/")
token = os.environ["CONFLUENCE_TOKEN"]
page_id = os.environ["CONFLUENCE_PAGE_ID"]
space_key = os.environ["CONFLUENCE_SPACE_KEY"]

wiki_files = Path("wiki").glob("*.md")

for wiki_file in wiki_files:
    title = wiki_file.stem        #stem removes .md from the wiki page name and print, so we can use that as confluence page
    print(f"Found Wiki page: {wiki_file} -> Confluence title: {title}")

# Read the GitHub Wiki

with open("wiki/Home.md", "r", encoding="utf-8") as file:
    markdown_content = file.read()

# convert Markdown to HTML

html_content = markdown.markdown(markdown_content)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
  }

# asking Confluence for the current version - so everytime a confluence page is edited and saved, confluence increases its version

response = requests.get(
  f"{confluence_url}/rest/api/content/{page_id}",
  params={"expand": "version"},
  headers=headers
)
response.raise_for_status()

page = response.json()

new_version = page["version"]["number"] + 1

# prepare the updated page

payload = {
    "id": page_id,
    "type": "page",
    "title": page["title"],
    "version": {
        "number": new_version
     },
     "body": {
         "storage": {
             "value": html_content,
             "representation": "storage"
      }
    }
}


# update the Confluence page

response = requests.put( 
  f"{confluence_url}/rest/api/content/{page_id}",
  headers=headers,
  json=payload
)
response.raise_for_status()

print("Confluence page updated successfully!")
             
