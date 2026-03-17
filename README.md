# URL Shortener (Bitly clone)

This project is a full-stack URL shortener web application built using Python with the FastAPI framework. It allows users to register and log in to a personal dashboard where they can convert long URLs into short, shareable links. When a URL is submitted, the system generates a unique short alias (or accepts a custom alias) and stores the mapping between the original and shortened link in a database using SQLAlchemy. The shortened link can then be used to redirect users to the original website. The application also tracks how many times each link is accessed and lets users manage their URLs through the dashboard, including copying links, generating QR codes for sharing, and deleting links they no longer need. The project demonstrates a complete workflow involving user authentication, backend API development, database integration, and a simple web interface for managing shortened links.

## Features

- User authentication (Register / Login)
- URL shortening
- Custom alias support
- Click tracking
- QR code generation
- Copy shortened link
- Delete URLs
- User dashboard

---

## Tech Stack

### Backend
- FastAPI
- Python
- SQLAlchemy
- JWT Authentication

## Repository structure 

URL_Shortener/
│
├── main.py
├── requirements.txt
│
├── Backend/
│   │
│   ├── database.py
│   │
│   ├── Models/
│   │   ├── models.py
│   │   └── user.py
│   │
│   ├── ViewModels/
│   │   ├── usercreate_schema.py
│   │   ├── userlogin_schema.py
│   │   └── URLrequest_schema.py
│   │
│   ├── Services/
│   │   ├── auth_service.py
│   │   ├── url_service.py
│   │   └── utils.py
│   │
│   └── Routers/
│       ├── ui_router.py
│       ├── user_router.py
│       ├── url_router.py
│       └── admin_router.py
│
├── Frontend/
│   │
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   └── admin.html
│   │
│   └── static/
│       ├── script.js
│       ├── admin.js
│       ├── styles.css
│       └── (qr library if any)
│
└── urls.db

## Setup and Usage

1. Clone the repository on your system

git clone https://github.com/Raunak-Dehankar/URL_Shortener.git
cd URL_Shortener

2. Create Virtual Environment and activate it

python -m venv venv
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Run the Backend Server
uvicorn Backend.main:app --reload

5. Open the Application in browser

http://127.0.0.1:8000

## Demo example

1. This is the first login page the user gets. Any user can login if they have an account or create a new one. 

![alt text](<images/initial login page-1.png>)

2. If an invalid user tries to login, they get an Invalid credentials error. 

![alt text](<images/invalid login-1.png>)

3. After clicking on the register link, the user is redirected to the registration window where they can register with new username, password and email ID. 

![alt text](<images/register webpage-1.png>)
![alt text](<images/register webpage-2.png>)

4. When the user is successfully registered, they are redirected to the login page when they can login with the new credentials. 

5. After successful login, the user can access the dashboard where they can create short links for multiple longer link, with or without alias. 

![alt text](<images/register webpage-3.png>)

6. If the alias is already available or dosen't meet the security standards, then no link is generated and Undefined error is shown. All the list the user has saved in the database is displayed in their links tab. User can cody or delete those links. 

![alt text](<images/succ link adding-1.png>)
![alt text](<images/incorrect or repeated link genrated-1.png>)

7. User can then create unique QR codes for their shortened links from the list to easily share via image. 

![alt text](<images/qr for shortened link-1.png>)

8. After the process is completed, user can logout which will save their progress. Logging out will redirect the webpage to login window. 

9. An Admin user can log into the login dashboard with predefined credentials. They have authority to view all links saved by each user, set a url generation limit on them and disable any user. 

Default Admin
Username: admin
Password: admin123

![alt text](<images/admin dashboard.png>)
![alt text](<images/disabled user with limit set.png>)