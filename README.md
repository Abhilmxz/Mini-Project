# 🚨 CivicEYE — Empowering Citizens to Report & Resolve Public Issues

CivicEYE is a modern web platform that connects **citizens** and **authorities** to improve communities through real-time issue reporting, tracking, and resolution.

> 🔍 See something broken? Report it.  
> 📍 Track it.  
> ✅ Watch it get resolved.

---

## 🌟 Vision

CivicEYE aims to **streamline civic engagement** by offering a transparent, easy-to-use system for the public to:
- Report public issues (like potholes, broken streetlights, etc.)
- Get updates on progress
- Enable municipal teams to respond faster and more efficiently

> ✨ **Civic technology** with real-world impact.

---

## ⚙️ Key Features

✅ **Smart Login System**  
Login using **email or username** — tailored for both users and admins.  
Admins are redirected to a dedicated dashboard.

✅ **Issue Reporting & Tracking**  
Simple forms for users to report problems. Real-time tracking and status updates.

✅ **Clean, Responsive UI**  
Mobile-friendly, accessible, and built with Tailwind CSS for modern aesthetics.

✅ **Role-Based Access**  
Admin and user roles handled securely with Django's authentication system.

✅ **Password Recovery & Registration**  
Includes forgot-password flow and new user sign-up.

---

## 🚀 Live Preview

🖥️ Coming Soon

---

## 🛠️ Tech Stack

| Layer       | Tools/Frameworks               |
|-------------|--------------------------------|
| Backend     | Django (Python)                |
| Frontend    | Django Templates + Tailwind CSS|
| Database    | SQLite (default, can upgrade)  |
| Auth System | Django Auth (customized logic) |

---

## 🧠 How It Works

1. Users land on a beautiful login screen
2. They enter their **email** (for users) or **username** (for admins)
3. Django authenticates and redirects them:
   - 🔐 Admin → `/adminover/`
   - 👤 User → `homelog`
4. Users can:
   - Submit issue reports
   - Track issue progress
5. Admins can:
   - View & manage all reports
   - Update statuses
   - Communicate with users

---

## 📂 Project Structure

civiceye/
├── templates/
│ └── login.html # Tailwind-powered login page
├── forms.py # Custom LoginForm (email or username)
├── views.py # Login logic with smart authentication
├── urls.py # URL routing
├── static/ # Static assets (CSS, JS, images)
├── requirements.txt # Python dependencies
└── README.md # You're here!
