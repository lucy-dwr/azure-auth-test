# SharePoint list fetcher

Fetches items from a SharePoint list via the Microsoft Graph API. Authentication uses the [device flow](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code) pattern — when you run the script, it prints a code and URL; you authenticate in a browser, and the script proceeds once auth is complete.

The target list is DWR's Science and Technology Partnerships Inventory on the `cawater.sharepoint.com` SharePoint site.

## Environment setup

Create a `.env` file at the repo root with the following values:

```bash
MS_CLIENT_ID=your-client-id
MS_TENANT_ID=your-tenant-id
```

These can be found in the Azure portal under your app registration.

## Quick start

From the repo root:

```bash
./scripts/setup.sh
```

This creates a project-local `.venv`, upgrades `pip`, and installs from `requirements.txt`.

## Running

Use the venv Python directly (no activation required):

```bash
.venv/bin/python fetch_sharepoint_list.py
```

Optional shell activation:

```bash
source .venv/bin/activate
python fetch_sharepoint_list.py
```

## Jupyter notebooks

If you are running code in a notebook, install dependencies into the notebook kernel environment:

```python
%pip install -r requirements.txt
```
