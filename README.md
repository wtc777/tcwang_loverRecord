# Couple Journal MVP

This repository contains a FastAPI backend and a Vue 3 + Element Plus frontend that together deliver a minimal couple journal application. The project is designed to run locally on Windows with PyCharm (backend) and Node.js tooling (frontend) without Docker.

## Project Structure

```
couple-journal/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ config.py
│  │  ├─ deps.py
│  │  ├─ db.py
│  │  ├─ models/
│  │  ├─ schemas/
│  │  ├─ routers/
│  │  ├─ services/
│  │  └─ utils/
│  ├─ .env.example
│  └─ requirements.txt
├─ frontend/
│  ├─ package.json
│  ├─ vite.config.ts
│  └─ src/
│     ├─ main.ts
│     ├─ router/
│     ├─ api/
│     ├─ pages/
│     └─ components/
└─ uploads/
   └─ assets/
```

## Backend Setup (FastAPI + SQLite)

1. Navigate to the backend folder and create/activate a Python 3.10+ virtual environment.
2. Install dependencies:
   ```powershell
   cd backend
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` if you need to override defaults.
4. Ensure the `uploads/assets` folder exists and place optional media such as `bgm.mp3`.
5. Run the API with Uvicorn (PyCharm run configuration or command line):
   ```powershell
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
6. Visit `http://localhost:8000/docs` to test routes. Register a user via `/api/auth/register` before logging in.

## Frontend Setup (Vue 3 + Vite)

1. Install dependencies with your preferred Node.js package manager (e.g. pnpm):
   ```powershell
   cd frontend
   pnpm install
   pnpm dev
   ```
2. Visit `http://localhost:5173` to access the UI. Start the romantic BGM from the login screen to satisfy browser autoplay policies.

## Key Features

* Authentication (register/login/profile) with JWT.
* Event CRUD with timeline display.
* Calendar and photo wall pages pulling data from the backend.
* Media upload pipeline with local storage and thumbnail generation for images.

## Notes

* Python code uses tab indentation to align with project conventions.
* Media uploads are stored under `uploads/` and referenced via absolute paths in responses.
* Update `FRONTEND_ORIGIN` in `.env` when hosting the frontend elsewhere.
