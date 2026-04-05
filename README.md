# Quiz Portal 🚀

A professional, high-security examination platform built with **React** and **Django**. This portal is designed for high-stakes testing with built-in proctoring and a modern dark-mode aesthetic.

---

## ✨ Key Features

### 🔒 Proctored Examination (Lockdown Mode)
- **Automatic Fullscreen:** Forces candidates into a focused, distraction-free environment.
- **Keyboard Protection:** Instantly terminates the exam if *any* unauthorized key is touched.
- **Tab Swapping Detection:** Automatically logs out users if they switch tabs.

### 📧 Secure Authentication
- **Multi-Step Signup:** Registration requires a 6-digit email OTP (One-Time Password) for verification.
- **Branded Communications:** All emails are professionally branded under the **QuizPortal** identity.
- **Simple Password Recovery:** Secure "Forgot Password" flow with email identification.

### 📐 Candidate Tools
- **Scientific Calculator:** A sleek, built-in calculator for complex mathematical processing.
- **Real-time Scoring:** Instant results and detailed performance reviews upon completion.

---

## 🛠️ Technology Stack

- **Frontend:** React 19 (Vite), React Router 7, Bootstrap 5, React Icons.
- **Backend:** Django 5, Django REST Framework, SimpleJWT.
- **Database:** SQLite (Default) with Supabase integration support.
- **Styling:** Premium Dark-Mode CSS with Glassmorphism effects.

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+**

### 2. Backend Setup
1. Navigate to the root directory.
2. Initialize and activate the virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```
   *Backend URL:* `http://localhost:8000/`

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd we/vite-project
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite server:
   ```bash
   npm run dev
   ```
   *Frontend URL:* `http://localhost:5173/` (Hardcoded strictly to this port).

---

## ⚙️ Configuration

### Email SMTP Setup
Edit `quiz_portal/settings.py` to configure your outgoing Gmail SMTP:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = '"QuizPortal" <your-email@gmail.com>'
```

### Environment Variables
Create a `.env` file in `we/vite-project/` for Supabase connection:
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_URL=http://localhost:8000/api
```

---

## 📂 Project Structure
```text
├── quiz/               # Django App (Logic, Models, Views)
├── quiz_portal/        # Django Project (Settings, URL Config)
├── we/
│   └── vite-project/   # React Frontend (Vite)
├── db.sqlite3          # Local Database
├── manage.py           # Django Utility
└── requirements.txt    # Python Dependencies
```

---

*Verified and Ready for Production Context.* 🎓
