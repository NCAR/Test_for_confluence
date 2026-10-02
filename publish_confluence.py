# load all libraries


import os              # os gets GitHub secret values
import requests        # requests talk to Confluence REST API
import markdown        # markdown converts GitHub Markdown into HTML
from pathlib import Path

# Getting values from GitHub Secrets

confluence_url = os.environ["CONFLUENCE_URL"].rstrip("/")
token = os.environ["CONFLUENCE_TOKEN"]
space_key = os.environ["CONFLUENCE_SPACE_KEY"]

wiki_files = Path("wiki").glob("*.md")

for wiki_file in wiki_files:
    
    title = wiki_file.stem        #stem removes .md from the wiki page name and print, so we can use that as confluence page

    #Read the current Wiki page
    
    with open(wiki_file, "r", encoding="utf-8") as file:
        markdown_content = file.read()

    # convert Markdown to HTML

    html_content = markdown.markdown(markdown_content)
    
    print(f"Found Wiki page: {wiki_file} -> Confluence title: {title}")

    response = requests.get(
        f"{confluence_url}/rest/api/content",
        params={
            "spaceKey": space_key,
            "title": title,
            "type": "page"
     },
     headers={
         "Authorization": f"Bearer {token}"
     }
   )

    response.raise_for_status()

    results = response.json()["results"]

    if results: 
        print(f"Page exist in Confluence: {title}")

        found_page_id = results[0]["id"]
        print(f"Found Confluence Page ID: {found_page_id}")

        # Get the current version
        
        response = requests.get(
           f"{confluence_url}/rest/api/content/{found_page_id}",
           params={"expand": "version"},
           headers={
               "Authorization": f"Bearer {token}"
           }
        )
        
        response.raise_for_status()

        page = response.json()
        new_version = page["version"]["number"] + 1

        # prepare the updated page

        payload = {
           "id": found_page_id,
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

        # update the existing Confluence page

        response = requests.put( 
            f"{confluence_url}/rest/api/content/{found_page_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"  
            },
            json=payload 
        )
    
        response.raise_for_status()

        updated_page = response.json()

        print(f"Updated Confluence page: {title}")
        print(f"Confluence returned version: {updated_page['version']['number']}")
             
    else:
        print(f"Page does not exist in Confluence: {title}")

        # Create a new Confluence page
        payload = {
           "type": "page",
           "title": title,            
           "space": {
               "key": space_key
           },
           "body": {
              "storage": {
                  "value": html_content,
                  "representation": "storage"
               }
             }
          } 
        response = requests.post( 
            f"{confluence_url}/rest/api/content",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"  
            },
            json=payload 
        )
    
        response.raise_for_status()

        print(f"Created Confluence page: {title}")
