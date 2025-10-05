# 🏢 NSSF Attachment and Internship Management Portal

A modern web platform designed to streamline **student industrial attachments** with **NSSF compliance** and secure digital management.  
Built with **Django**, styled using the **NSSF theme** (trustworthy, professional, and accessible).

---

## 🚀 Features

- 🔐 **Secure Authentication** — Role-based login for students, supervisors, and administrators.  
- 📄 **Attachment Management** — Track and approve student attachment requests.  
- 🏢 **Company Integration** — Manage company profiles and placement opportunities.  
- 💬 **Real-time Notifications** — Stay updated with approvals, feedback, and deadlines.  
- 🎨 **Custom NSSF UI Theme** — Professional, clean, and responsive interface inspired by NSSF colors and values.  
- 📊 **Dashboard Insights** — View key attachment statistics and analytics.  

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Django (Python 3.10+) |
| Frontend | Bootstrap 5, Font Awesome 6 |
| Database | PostgreSQL / MySQL |
| Styling | Custom CSS (`nssf-theme.css`) |
| Hosting | Render / Docker Ready |

---

## 🛠️ Setup Instructions


# 1️⃣ Clone the repository
git clone https://github.com/jacksonochieng1540/nssf-attachment-portal.git
cd nssf-attachment-portal

# 2️⃣ Create a virtual environment
python -m venv venv #windows
python3 -m venv venv
source venv/bin/activate -linux  # (Windows: venv\Scripts\activate)

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Configure environment variables
cp .env.example .env
# Update your DB credentials, SECRET_KEY, and DEBUG settings

# 5️⃣ Run migrations
python manage.py migrate

# 6️⃣ Start the development server
python manage.py runserver

🛡️ License

This project is licensed under the MIT License
.
Feel free to use and modify it for your own projects — attribution appreciated.
