# NSSF Attachment and Internship Management Portal

A modern web platform designed to streamline **student industrial attachments** with **NSSF compliance** and secure digital management.  
Built with **Django**, styled using the **NSSF theme** (trustworthy, professional, and accessible).


#  Composition of the project

-**Secure Authentication** — Role-based login for students, Company and administrators(admin).  
-**Attachment Management** — Track and approve student attachment requests.  
-**Company Integration** — Manage company profiles and placement opportunities.  
-**Real-time Notifications** — Stay updated with approvals, feedback, and deadlines of the attachment and Internships.  
-**Custom NSSF UI Theme** — Professional, clean, and responsive interface inspired by NSSF colors and values.  
-**Dashboard Insights** — View key attachment statistics and analytics.  

|

##  To  Setup follow the below  Instructions


# Clone the repository
git clone https://github.com/jacksonochieng1540/nssf-attachment-portal.git
cd nssf-attachment-portal

#  Create a virtual environment
python -m venv venv #windows
python3 -m venv venv
source venv/bin/activate -linux  # (Windows: venv\Scripts\activate)

#  Install dependencies
pip install -r requirements.txt

#  Configure environment variables
cp .env.example .env
# Update your DB credentials, SECRET_KEY, and DEBUG settings

#  Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver

