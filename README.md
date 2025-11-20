# RLCAPTCHA



# Set Up Guide

Install PostgresSQL

Backend
```bash
cd backend

Windows:
python3 -m venv .venv
.venv/Scripts/activate
Mac:
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

create .env file
    PSQL_PASSWORD=your-psql-password
```

```bash
pyhton3 create_database.py
python3 main.py
```