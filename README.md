# Hospital Management API

A Django REST Framework project for managing patients and medical records in a hospital setting. Built for assignment purposes.

## Tech Stack
- Python 3
- Django 4+
- Django REST Framework
- SimpleJWT (for authentication)

## Features
- Doctor and admin user roles
- Patient management (CRUD)
- Medical record management
- JWT authentication
- Permissions: Doctors can only access their own patients/records; admins can access all
- Unit tests for core business logic

## Setup
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt
   ```
3. **Apply migrations**
   ```bash
   python hospital_api/manage.py makemigrations core
   python hospital_api/manage.py migrate
   ```
4. **Create a superuser (admin)**
   ```bash
   python hospital_api/manage.py createsuperuser
   ```
5. **Run the server**
   ```bash
   python hospital_api/manage.py runserver
   ```

## API Endpoints
All endpoints are prefixed with `/api/`.

### Authentication
- `POST /api/signup/` — Register a new doctor
- `POST /api/login/` — Obtain JWT token

### Patients (Doctor only)
- `POST /api/patients/` — Create a new patient
- `GET /api/patients/` — List your patients
- `GET /api/patients/<id>/` — Patient detail
- `GET /api/patients/<id>/records/` — List medical records for a patient
- `POST /api/patients/<id>/add_record/` — Add a medical record to a patient

### Medical Records
- `GET /api/records/` — List your patients' records
- `POST /api/records/` — Add a record (for your own patients)

### Admin Access
- Superusers can view all patients and records

## Testing
Run all tests:
```bash
python hospital_api/manage.py test core
```

## Notes
- All endpoints require JWT authentication except signup/login.
- Doctors can only access their own patients and records.
- Admins (superusers) can access all data.

## License
MIT 