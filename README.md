# Alerts Monitoring Dashboard

A full-stack alerts monitoring system built with **React (TypeScript)** and **Django**, designed to help managers monitor, filter, and act on employee alerts efficiently.

This project was completed as a **take-home engineering assignment** and is also maintained as a **portfolio project** to demonstrate clean architecture, real-world UX considerations, and backend-frontend integration.

---
![dashboard](https://github.com/user-attachments/assets/de4368b6-61a4-4e30-9967-a2b75343c9b3)

## 🖼️ Dashboard Preview



```md
![dashboard](https://github.com/user-attachments/assets/afabf9d1-1cf9-4436-b3ac-add041847797)

```

_(Create a `screenshots/` folder in the root and add your image there.)_

---

## 🚀 What This Project Does

The Alerts Monitoring Dashboard allows a manager to:

- View alerts generated for employees
- Filter alerts by **scope**, **severity**, and **status**
- Search alerts by employee name
- Paginate large alert lists
- Dismiss alerts (idempotent action)
- Switch between **direct reports** and **entire subtree**

The UI is clean, responsive, and optimized for clarity and speed.

---

## 🧠 Key Engineering Decisions

### Frontend
- Built with **React + TypeScript**
- Fully controlled filter state
- Debounced search input for performance
- Clear loading, empty, and error states
- Pagination handled cleanly without UI jank
- TailwindCSS for fast, consistent styling

### Backend
- Built with **Django**
- Clean data modeling using self-referential relationships
- Optimized queries using indexes
- Deterministic seed data for easy testing
- REST-style API endpoints

---

## 🏗️ Project Structure

```
alerts-monitoring-dashboard/
│
├── alerts-frontend/        # React + TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   ├── api/
│   │   ├── types/
│   │   └── App.tsx
│   └── package.json
│
├── backend/                # Django backend
│   ├── alerts/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── fixtures/
│   │   │   └── seed_data.json
│   └── manage.py
│
├── .gitignore
└── README.md
```

---

## 🧩 Core Features

### ✅ Filtering
- Scope: **Direct Reports** / **Subtree**
- Severity: Low / Medium / High
- Status: Open / Dismissed

### 🔍 Search
- Search alerts by employee name
- Debounced input to reduce unnecessary requests

### 📄 Pagination
- Server-side pagination
- Clear navigation controls
- Accurate total counts

### 🔕 Alert Dismissal
- Idempotent dismiss action
- UI updates immediately after dismissal
- Prevents duplicate state changes

---

## 🗃️ Data Model Overview

### Employee
- Self-referential relationship to support org hierarchy
- Enables subtree traversal

### Alert
- Linked to an employee
- Severity and status enums
- Indexed fields for performance

---

## ⚙️ Getting Started (Local Setup)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Gwerdonatus/alerts-monitoring-dashboard.git
cd alerts-monitoring-dashboard
```

---

## 🐍 Backend Setup (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Load Seed Data

```bash
python manage.py loaddata seed_data.json
```

### Start Backend Server

```bash
python manage.py runserver
```

Backend runs at:  
**http://localhost:8000**

---

## ⚛️ Frontend Setup (React)

```bash
cd alerts-frontend
npm install
npm start
```

Frontend runs at:  
**http://localhost:3000**

---

## 🧪 Seed Data Details

- Includes **7+ employees**
- Includes multiple alerts with mixed:
  - severities
  - statuses
  - timestamps
- Default manager ID used by frontend:
  ```
  MGR001
  ```

This allows immediate testing of:
- filtering
- pagination
- subtree vs direct reports

---

## 🧼 Production Build

```bash
npm run build
```

Build output is optimized and ready for deployment.

---

## 🔐 Security & Best Practices

- No secrets committed
- Environments properly ignored via `.gitignore`
- Clean separation between frontend and backend
- Idempotent backend operations
- Predictable seed data for reviewers

---

## 📌 Possible Enhancements

- Authentication & role-based access
- Real-time updates (WebSockets)
- Alert creation UI
- Audit logs
- Export functionality

---

## 👤 Author

**Gwer Msughter Donatus**  
Full-Stack Developer (Python / Django / React)

- GitHub: https://github.com/Gwerdonatus
- LinkedIn: https://www.linkedin.com/in/donatus-gwer-857610338

---

## 📄 License

This project is provided for demonstration and evaluation purposes.

