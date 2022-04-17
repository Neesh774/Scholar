# Scholar

An app that scans your Google Classroom assignments and puts them into a Notion Calendar.

## Usage

### Keys

Create a Google Cloud account with these two links:

- https://developers.google.com/workspace/guides/create-project
- https://developers.google.com/workspace/guides/create-credentials
  Then, create a Notion integration here:
- https://www.notion.so/my-integrations
  Make sure the integration has access to your database by inviting it with the share button in Notion

### Files

`credentials.json`

```
{
  "installed": {
    "client_id": "",
    "project_id": "",
    "auth_uri": "",
    "token_uri": "",
    "auth_provider_x509_cert_url": "",
    "client_secret": "",
    "redirect_uris": ["http://localhost"]
  }
}
```

`keys.json`

```
{
  "type": "",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": "",
  "notion": "notion integration secret",
  "database": "database id",
}
```

### Notion Properties

Ensure that your Notion database has the following properties

- Date (Date)
- Progress (Single Select with options Completed, In Progress, and Unstarted)
- Subject (Text)
- id (Text)

### Running

Run the `scholar.py` file to get started :)

<h3 align="center">🙋‍♂️ Made by <a href="https://twitter.com/Neesh774">@Neesh774</a></h3>
<p align="center">
  <a href="https://www.buymeacoffee.com/ilioslabs" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-violet.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" >
  </a>
</p>
