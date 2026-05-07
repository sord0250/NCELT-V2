# NCELT Evidence Tracking App

NCELT is a local web application for organizing cybersecurity compliance evidence. Its overarching goal is to help a team track evidence files, map each piece of evidence to NIST Cybersecurity Framework (CSF) 2.0 outcomes/controls, assign clear ownership, and manage evidence lifecycle by tracking last-reviewed and next-review dates.

The app is designed around a practical Governance, Risk, and Compliance (GRC) workflow: collect evidence, connect it to framework requirements, identify who owns it, and monitor whether the evidence is current enough to support reviews, audits, or internal compliance checks.

## What This App Does

- Tracks uploaded evidence files in a local evidence repository.
- Maps evidence to one or more NIST CSF 2.0 outcomes/subcategories.
- Assigns each evidence item to an owner, such as a person, team, or department.
- Tracks the last-reviewed date and lifecycle length for each evidence item.
- Calculates next-review dates so users can see which evidence is current, approaching review, or overdue.
- Provides an Evidence Dashboard for reviewing evidence by owner and review status.
- Provides a Framework Dashboard for viewing NIST outcomes, linked evidence, missing evidence, and review timing.
- Supports manager/user account creation with password hashing and session-based authentication.

## Technical Implementation

NCELT is implemented as a Python web application using FastAPI, SQLAlchemy, SQLite, and Jinja2 templates.

### Core Stack

- **FastAPI**: Defines the web application, routes, authentication flow, upload workflow, dashboards, and evidence detail pages.
- **SQLAlchemy**: Provides the object-relational mapping layer for users, owners, NIST outcomes, evidence records, and evidence-to-outcome relationships.
- **SQLite**: Stores application data locally in `nceltt.db`.
- **Jinja2**: Renders HTML templates for dashboards, upload forms, login/setup pages, and detail views.
- **Passlib**: Hashes and verifies user passwords.
- **Starlette SessionMiddleware**: Maintains authenticated user sessions.
- **Uvicorn**: Runs the local development server.

### Data Model

The app uses five main data concepts:

- **User**: An application account. Manager users can create additional users.
- **Owner**: The person, team, or group responsible for a piece of evidence.
- **Outcome**: A NIST CSF 2.0 framework outcome/subcategory, identified by a subcategory ID such as `GV.OC-01` or `ID.RA-05`.
- **Evidence**: An uploaded file with a title, description, owner, review dates, lifecycle length, and mapped outcomes.
- **Supports**: A join table that allows each evidence item to support multiple NIST outcomes, and each NIST outcome to have multiple evidence items.

### Main Features

- **Authentication and setup**: The `/setup` route creates the first manager account. Users then log in through `/login`.
- **Evidence upload**: The `/upload` route lets users upload a file, select an owner, map NIST outcomes, set a last-reviewed date, and define a lifecycle length.
- **Evidence dashboard**: The `/` route lists uploaded evidence and allows filtering by owner and review status.
- **Framework dashboard**: The `/framework` route lists NIST outcomes and shows whether evidence is present, missing, current, or approaching review.
- **Evidence detail view**: The `/evidence-record/{evidence_id}` route shows owner, mapped outcomes, review dates, and the uploaded evidence file.
- **Review updates**: Users can update the last-reviewed date for an evidence record to keep lifecycle status current.
- **File storage**: Uploaded files are stored locally under `data/evidence`.

### Review Status Logic

Each evidence item has a last-reviewed date and lifecycle length. The app calculates the next-review date from those fields and assigns a status:

- **Green**: Evidence is current.
- **Yellow**: Evidence is within 21 days of review.
- **Red**: Evidence is within 3 days of review or past due.

This gives users a simple way to prioritize which evidence needs attention before a review or audit.

## How To Run The App

These steps assume Python is already installed.

### 1. Create and activate a virtual environment

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Start the local server

```powershell
python -m uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

### 4. Create the first manager account

On the first run, go to:

```text
http://127.0.0.1:8000/setup
```

Create the initial manager account. After that, the app will redirect users to the login page.

### 5. Load starter framework data

To load starter owners and NIST CSF 2.0 outcomes, run:

```powershell
python -m app.seed
```

This seeds the database with example owners and NIST outcomes across the Govern, Identify, Protect, Detect, Respond, and Recover functions.

## How To Use The App

1. **Log in**

   Sign in with the manager account created during setup.

2. **Create evidence owners**

   Go to **Create Owner** and add the people, teams, or departments responsible for maintaining evidence.

3. **Upload evidence**

   Go to **Upload Evidence** and provide:

   - Evidence title
   - Description
   - Owner
   - One or more mapped NIST CSF 2.0 outcomes
   - Last-reviewed date
   - Lifecycle length in months
   - Evidence file

4. **Review the Evidence Dashboard**

   Use the Evidence Dashboard to view uploaded evidence, assigned owners, mapped outcomes, last-review dates, next-review dates, and evidence file links.

5. **Review the Framework Dashboard**

   Use the Framework Dashboard to see NIST outcomes and determine which outcomes already have evidence, which are missing evidence, and which evidence items are approaching review.

6. **Update evidence reviews**

   Open an evidence record and update the last-reviewed date when the evidence has been reviewed or refreshed.

7. **Use dashboards for GRC planning**

   Use owner filters, evidence presence filters, and review-status indicators to plan evidence collection, prepare for audits, and maintain control coverage over time.

## Project Structure

```text
NCELT/
|-- app/
|   |-- main.py              # FastAPI routes, auth flow, dashboards, uploads
|   |-- models.py            # SQLAlchemy data models and relationships
|   |-- crud.py              # Database helper functions
|   |-- db.py                # SQLite and SQLAlchemy setup
|   |-- seed.py              # Starter owners, users, and NIST outcomes
|   |-- static/              # CSS styles
|   `-- templates/           # Jinja2 HTML templates
|-- data/
|   `-- evidence/            # Uploaded evidence files
|-- documentation/           # Screenshots, schema, and app structure docs
|-- requirements.txt         # Python dependencies
|-- nceltt.db                # Local SQLite database
`-- README.md
```

## Notes

- This app is intended for local use and learning/prototyping.
- For production use, replace the development session secret, enable HTTPS-only cookies, use a production database, add backup/retention controls, and review access control requirements.
- NIST CSF 2.0 uses functions, categories, and subcategories/outcomes. This app uses those outcomes as the framework mapping layer for evidence.
