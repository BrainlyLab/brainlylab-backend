# brainlylab-backend

## Steps to Set up the backend on your local device:
### 1️⃣ Clone the repository

```bash
cd "Path to wherever you want to clone it."
git clone <repo-url>
cd brainlylab-backend
```

---

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

---

### 3️⃣ Activate the virtual environment (Windows)

```bash
.\venv\Scripts\activate
```

Terminal shows:

```
(venv)
```

---

### 4️⃣ Install project dependencies

```bash
pip install -r requirements.txt
```

This installs Django and other required libraries.

---

### 5️⃣ Create the `.env` file

Copy the example environment file:

```bash
copy .env.example .env
```

---

### 6️⃣ Edit `.env` with PostgreSQL credentials

Example:

```
DB_NAME=brainlylab
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

---

### 7️⃣ Install PostgreSQL

Install:

* PostgreSQL server
* pgAdmin

PostgreSQL runs the database.

pgAdmin is the GUI tool to manage it.

---

### 8️⃣ Create the database in pgAdmin

Inside pgAdmin:

```
Servers
  → PostgreSQL
      → Databases
          → Create Database
```

Database name:

```
brainlylab
```

---

### 9️⃣ Apply Django migrations

This creates tables in the database.

```bash
python manage.py migrate
```

You saw many lines like:

```
Applying auth.0001_initial... OK
```

---

### 🔟 Start the backend server

```bash
python manage.py runserver
```

Server runs at:

```
http://127.0.0.1:8000
```

---

# Final Architecture You Built

```
GitHub Repo
     ↓
Virtual Environment
     ↓
Django Backend
     ↓
PostgreSQL Database
     ↓
Local Server (127.0.0.1:8000)
```

---

# Quick Developer Command Summary

If you open the project again, you only need:

```bash
cd brainlylab-backend
.\venv\Scripts\activate
python manage.py runserver
```

---

