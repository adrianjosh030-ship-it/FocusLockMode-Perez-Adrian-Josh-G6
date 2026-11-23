# Focus Lock Mode (IM2 Project)

Full-stack Django + PostgreSQL/Supabase.

- **Phase 1 (PD1):** Account Feature: registration, login/logout, role-based dashboards, user profile.
- **Phase 2 (PD2):** Core Feature: **Focus Sessions** (vertical slice).

Roles: **Admin** and **Student**.

## Core Feature: Focus Sessions
Students plan and run timed focus sessions, and admins can monitor all sessions.

- **Create** a session with a title, optional category, planned minutes, and notes.
- **Read** your sessions in a list (filterable by status) and a detail page.
- **Update** a session while it is planned or active.
- **Delete** a session, with a confirmation step.
- **Workflow:** Planned, then Start focus, then Complete or Abandon.
- **Categories:** each student creates their own categories (e.g. "Math").

### Validation and business rules
- Title is required and must be at least 3 characters.
- Planned time must be between 5 and 240 minutes.
- Only one active session per user at a time.
- Finished (completed or abandoned) sessions cannot be edited.
- Clear success and error messages are shown for every action.

### Access control
- Only logged-in users can access the feature.
- Every record is linked to its creator (ForeignKey to User).
- Students can only view and modify their own sessions. Other users' session URLs return 404.
- Admins can view and manage all sessions.
- The feature is linked from both the Student and Admin dashboards.

### Models
- `Category` (user FK to User, name)
- `FocusSession` (user FK to User, category FK to Category, title, planned_minutes, status, notes, started_at, ended_at, created_at)

## Setup (Windows PowerShell)
```
git clone https://github.com/adrianjosh030-ship-it/FocusLockMode-Perez-Adrian-Josh-G6.git
cd FocusLockMode-Perez-Adrian-Josh-G6
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env      # then edit .env (SECRET_KEY + database)
python manage.py migrate
python manage.py createsuperuser # superusers are automatically Admins
python manage.py runserver
```
If port 8000 is blocked on Windows, use `python manage.py runserver 8080`.

## URLs
- `/accounts/register/`, `/accounts/login/`
- Admin dashboard: `/accounts/dashboard/admin/`
- Student dashboard: `/accounts/dashboard/student/`
- Profile: `/accounts/profile/`
- Focus sessions: `/focus/`
- New session: `/focus/new/`
- New category: `/focus/categories/new/`

## Tests
`python manage.py test accounts`