import os.path
from pathlib import Path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googledrive import find_docs_id # type: ignore 
# If modifying these scopes, delete the file token.json.

# The ID of a sample document.


def get_google_doc_as_dict(title_name):
  SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]
  DOCUMENT_ID = find_docs_id(title_name)
  """Shows basic usage of the Docs API.
  Prints the title of a sample document.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("tokendocs.json"):
    creds = Credentials.from_authorized_user_file("tokendocs.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("tokendocs.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("docs", "v1", credentials=creds)

    # Retrieve the documents contents from the Docs service.
    # document = service.documents().get(documentId=DOCUMENT_ID).execute()

    # print(f"The title of the document is: {document.get('title')}")
    result = service.documents().get(documentId=DOCUMENT_ID).execute()
    #with open("sample.json", "w") as outfile:
    #  outfile.write(json.dumps(result, indent=4, sort_keys=True))
    #print(result)
    return result

    # print(json.dumps(result, indent=4, sort_keys=True))
  except HttpError as err:
    print(err)

def return_links_and_titles(title_name):
  titles = []
  links = []
  doc_dict = get_google_doc_as_dict(title_name)
  links_between_title = []
  #print(doc_dict["body"]["content"][1]) 
  for doc_lines in doc_dict["body"]["content"]:
    if "paragraph" in doc_lines:
      if "paragraphStyle" in doc_lines["paragraph"]:
        if "namedStyleType" in doc_lines["paragraph"]["paragraphStyle"]:
          # Check for a Title:
          if doc_lines["paragraph"]["paragraphStyle"]["namedStyleType"] == "HEADING_2":
            if len(titles) > 0:
              links.append(links_between_title)
              links_between_title = []
            title = doc_lines["paragraph"]["elements"][0]["textRun"]["content"]
            if title[0].isdigit():
              if title[1].isdigit():
                if title[2].isdigit():
                  title = title[4:]     
                else:
                  title = title[3:]     
              else:
                title = title[2:]     
            titles.append(title)

          # Check for a Link:
          elif "link" in doc_lines["paragraph"]["elements"][0]["textRun"]["textStyle"]:
            links_between_title.append(convert_affiliate_links(doc_lines["paragraph"]["elements"][0]["textRun"]["textStyle"]["link"]["url"]))
  links.append(links_between_title)
  return (titles,links)
  print(links[2])

def convert_affiliate_links(affiliate_link):
  # example file path can be used for github
  # shouldn't contain sensitive information if
  # you plan to upload it to github
  file_path = Path('affiliate_links.json') 
  example_file_path = Path('example_affiliate_links.json') 

  if file_path.exists(): 
    with file_path.open('r') as file: 
      links = json.load(file)
  elif example_file_path.exists(): 
    with example_file_path.open('r') as file: 
      links = json.load(file)
  
  if affiliate_link.startswith("https://amzn.to"):
    affiliate_link = "Amazon " + affiliate_link
  elif affiliate_link.startswith("https://www.idealo.de"):
    affiliate_link = (links['links'][0] + affiliate_link)
  elif affiliate_link.startswith("https://www.mediamarkt.de/"):
    affiliate_link = (links['links'][1] + affiliate_link)
  return affiliate_link

if __name__ == "__main__":
  print(convert_affiliate_links("https://www.mediamarkt.de/de/product"))
  # print(return_links_and_titles("Speicher")[0][1])