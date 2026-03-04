"""
Authenticates to Microsoft Graph via device flow and fetches items from a
SharePoint list. Reads MS_CLIENT_ID and MS_TENANT_ID from a .env file.
"""

import os
import msal
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("MS_CLIENT_ID")
TENANT_ID = os.getenv("MS_TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

SCOPES = ["Sites.Read.All"]

LIST_NAME = "DWR's Science and Technology Partnerships Inventory"
GRAPH_ENDPOINT = (
    "https://graph.microsoft.com/v1.0"
    "/sites/cawater.sharepoint.com:/sites/dwr-ecc:"
    f"/lists/{quote(LIST_NAME)}/items?$expand=fields"
)

def get_token():

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY
    )

    flow = app.initiate_device_flow(scopes=SCOPES)

    if "user_code" not in flow:
        raise Exception("Device flow failed")

    print(flow["message"])

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        raise Exception(result)

    return result["access_token"]


def main():

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(GRAPH_ENDPOINT, headers=headers)

    print("\nGraph response status:", response.status_code)
    print("\nList items returned by Microsoft Graph:\n")
    print(response.json())


if __name__ == "__main__":
    main()