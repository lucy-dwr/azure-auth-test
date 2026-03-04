"""
Authenticates to Microsoft Graph via device flow and fetches items from a
SharePoint list. Reads MS_CLIENT_ID and MS_TENANT_ID from a .env file.

Tokens are cached in .token_cache.json so re-authentication is only needed
if the cache is missing or the refresh token has expired.
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

TOKEN_CACHE_FILE = ".token_cache.json"

LIST_NAME = "DWR's Science and Technology Partnerships Inventory"
GRAPH_ENDPOINT = (
    "https://graph.microsoft.com/v1.0"
    "/sites/cawater.sharepoint.com:/sites/dwr-ecc:"
    f"/lists/{quote(LIST_NAME)}/items?$expand=fields"
)


def load_cache():
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE, "r") as f:
            cache.deserialize(f.read())
    return cache


def save_cache(cache):
    if cache.has_state_changed:
        with open(TOKEN_CACHE_FILE, "w") as f:
            f.write(cache.serialize())


def get_token():
    cache = load_cache()

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache
    )

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            save_cache(cache)
            return result["access_token"]

    flow = app.initiate_device_flow(scopes=SCOPES)

    if "user_code" not in flow:
        raise Exception("Device flow failed")

    print(flow["message"])

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        raise Exception(result)

    save_cache(cache)
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
