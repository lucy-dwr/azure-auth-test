# Registering a Microsoft Entra application for Microsoft Graph access

These instructions describe how to register an application in **Microsoft Entra ID** and configure it so a script can authenticate and access resources through the **Microsoft Graph API**.

Microsoft Graph provides a unified endpoint for Microsoft 365 services including SharePoint, Teams, OneDrive, Outlook, Planner, and more. Any of these can be accessed once an app registration is in place.

The goal is to obtain two identifiers that a script will use to authenticate:

- **Application (client) ID**
- **Directory (tenant) ID**

---

## 1. Open Microsoft Entra App Registrations

Navigate to:

> Microsoft Entra admin center → Applications → App registrations → New registration

---

## 2. Register the application

Fill out the form as follows.

**Name** — choose something descriptive for the script or integration, for example: `graph_api_client`

**Supported account types** — select your tenant (single tenant is appropriate for internal scripts): "Accounts in this organizational directory only"

**Redirect URI** — leave blank.

Click **Register**.

---

## 3. Record the application identifiers

After registration you will land on the **Overview** page. Copy and save the **Application (client) ID** and **Directory (tenant) ID**.

These are typically stored as environment variables:

```sh
MS_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
MS_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Generally, you should not commit environment variables to a public repository!

---

## 4. Enable public client authentication

For scripts that authenticate interactively using **device code flow**, the app must allow public client authentication.

Navigate to:

> Authentication → Advanced settings

Set **Allow public client flows** to **Yes**, then save.

_Skip this step if you are using a client secret or certificate instead of device code flow._

---

## 5. Grant Microsoft Graph permissions

Navigate to:

> API permissions → Add a permission → Microsoft Graph → Delegated permissions

Add the permissions your script requires. Examples by use case:

| Use case | Permission(s) to add |
|---|---|
| Read SharePoint sites and lists | `Sites.Read.All` |
| Read/write SharePoint | `Sites.ReadWrite.All` |
| Read user's files (OneDrive) | `Files.Read.All` |
| Read Teams data | `Team.ReadBasic.All` |
| Read Outlook mail | `Mail.Read` |
| Read calendar | `Calendars.Read` |

`User.Read` is added automatically and allows reading the signed-in user's profile.

Choose the minimum permissions needed for your use case.

---

## 6. Confirm consent status

In some enterprise tenants, delegated permissions **do not require admin consent**.

If the permissions table shows **Admin consent required: No**, no further approval is needed — the user will be prompted to consent on first login.

If admin consent is required, an administrator must click **Grant admin consent** in the API permissions panel before the app can be used.

---

## 7. Provide credentials to the script

Pass the two identifiers to your script via environment variables:

```sh
MS_CLIENT_ID=<Application client ID>
MS_TENANT_ID=<Directory tenant ID>
```

Python scripts commonly use the **MSAL library** to obtain an access token and call Microsoft Graph.

---

## 8. What happens at authentication time (device code flow)

When a script using device code flow runs for the first time, the following sequence occurs:

1. **The script requests a device code** from Microsoft Entra using the client ID and tenant ID.

2. **The script prints instructions** to the terminal, for example:

   > To sign in, use a web browser to open https://microsoft.com/devicelogin and enter the code **ABCD1234** to authenticate.

3. **Open the URL in a browser** and enter the code. Sign in with your organizational account if prompted.

4. **Consent or approval** — Microsoft displays the permissions the app is requesting. What happens next depends on your tenant's policy:
   - If no admin consent is required, you can approve immediately and the script proceeds.
   - In stricter enterprise environments, you may be asked to provide a **business justification** for why you need access. The request is then routed to an IT administrator for review. You will typically receive an email notification when it is approved or denied.

5. **Once approved**, the script receives an access token and begins making API calls. Subsequent runs reuse a cached token and skip this process until the token expires.

---

## Result

After completing these steps, a script can:

1. Authenticate a user via Microsoft Entra (device code flow or other)
2. Obtain a Microsoft Graph access token
3. Call any Graph API endpoint the app has been granted permission to access
