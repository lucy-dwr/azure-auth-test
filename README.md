# SharePoint list fetcher

Fetches items from a SharePoint list via the Microsoft Graph API.

The target list is DWR's Science and Technology Partnerships Inventory on the `cawater.sharepoint.com` SharePoint site.

> [!WARNING]
> Production authentication and authorization must align with IT security requirements. The local commands in this repository are for development/testing only and are not the approved production access pattern.

## Target architecture

This project is expected to align to the following model:

- App-only authentication using a confidential client
- Certificate-based authentication in a controlled runtime (for example Azure Function or managed VM)
- Site-scoped SharePoint access using `Sites.Selected` and per-site grants (not tenant-wide read scope)
- Enterprise App sign-in gating, Conditional Access, secure token handling, and monitoring/governance controls

See [IT Security Requirements for SharePoint Graph Access](docs/it-auth-security-requirements.md) for the full requirements and implementation expectations.

## Documentation

- [IT Security Requirements for SharePoint Graph Access](docs/it-auth-security-requirements.md) is the source of truth for required controls.
- [Registering a Microsoft Entra application for Microsoft Graph access](docs/entra-setup.md) provides Entra setup steps; validate all production decisions against the IT requirements document.

## Environment setup (local development)

Create a `.env` file at the repo root with the following values:

```bash
MS_CLIENT_ID=your-client-id
MS_TENANT_ID=your-tenant-id
```

These can be found in the Azure portal under your app registration. See [docs/entra-setup.md](docs/entra-setup.md) for instructions on creating one.

## Quick start

From the repo root:

```bash
./scripts/setup.sh
```

This creates a project-local `.venv`, upgrades `pip`, and installs from `requirements.txt`.

## Running

> [!CAUTION]
> These local run steps are for development/testing. For production approval and deployment, follow [docs/it-auth-security-requirements.md](docs/it-auth-security-requirements.md).

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
