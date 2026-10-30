# Interior designer workspace

Start the existing Flask application with `python app.py`. On the login screen,
select Interior Designer and sign in with an existing active designer account.
User Admin can create a designer account through the existing account form.
No sample accounts or passwords are added by this feature.

The designer landing page is `/interior-designer/company`. Create company
information there, then use Projects to manage ongoing and completed projects.
Company and project forms, search, status filters, name sorting, pagination,
suspension, reactivation, and confirmed logout use the Flask backend.
Projects are paged in groups of five. Completed projects require an end date
on or after the start date. Cancel leaves saved records unchanged.

The new Entity, Controller, and Boundary use the existing account database and
login controller. Tables `designer_companies` and `design_projects` are created
automatically on startup without replacing existing account records.
All designer routes validate the logged-in account and assigned profile,
scope records to the designer, and protect form submissions with CSRF tokens.

Set `RENOVO_SECRET_KEY` to a stable private value when running across restarts
or multiple workers. Without it, startup generates a temporary signing key,
so restarting the server ends existing sessions.

The current account schema has no company membership relationship. Each
designer therefore owns one company and its project portfolio; the designer
list contains that owner. Sharing a company among several designer accounts
requires a membership model. Suspension is persisted here; a future customer
listing must filter out suspended companies and projects before displaying them.

Run the integration checks with:

```powershell
python -B -m unittest discover -s tests -v
```

Tests use temporary databases and do not modify the application's account data.
