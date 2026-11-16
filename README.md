# Focus Lock Mode (IM2 Project)

Full-stack Django + PostgreSQL/Supabase. Phase 1: Account Feature
(registration, login/logout, role-based dashboards, user profile).

Roles: **Admin** and **Student**.

## Setup (Windows PowerShell)
```
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env      # then edit .env (SECRET_KEY + database)
python manage.py migrate
python manage.py createsuperuser # superusers are automatically Admins
python manage.py runserver
```

## URLs
- `/accounts/register/`, `/accounts/login/`
- Admin dashboard: `/accounts/dashboard/admin/`
- Student dashboard: `/accounts/dashboard/student/`
- Profile: `/accounts/profile/`

## Tests
`python manage.py test accounts`
