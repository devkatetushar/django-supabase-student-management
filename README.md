# Colourful Django Student Portal + Supabase

## Pages
- `/` — colourful home page with Student and Admin entry points.
- `/student/login/` — student sign-in.
- `/student/dashboard/` — student's own linked profile.
- `/manage/` — student CRUD, restricted to staff users.
- `/admin/` — separate Django admin login.

## Setup
1. Copy `.env.example` to `.env` beside `manage.py`.
2. Replace `DATABASE_URL` with the real PostgreSQL URL from Supabase Connect.
3. Run from the folder containing `manage.py`:
   `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
   `.\.venv\Scripts\python.exe manage.py check`
   `.\.venv\Scripts\python.exe manage.py makemigrations school`
   `.\.venv\Scripts\python.exe manage.py migrate`
   `.\.venv\Scripts\python.exe manage.py createsuperuser`
   `.\.venv\Scripts\python.exe manage.py runserver`

PowerShell activation is not required. Keep `.env` private. If DATABASE_URL is blank, the project falls back to SQLite.

## Student account setup
Log in at `/admin/` as superuser, create a normal user (not staff), then edit/create the corresponding Student record and select that user in the User account field. The student can then use `/student/login/`. Staff can use `/manage/` and `/admin/`.
