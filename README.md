# ✍️ Inkwell – Django Blogging Platform

**Inkwell** is a full-featured blogging platform built with Django, offering authenticated user access, post creation/editing/deletion, threaded comments, and admin controls. Designed with Bootstrap for a clean UI.

---

## 🚀 Features

- 🔐 **User Authentication**

  - Register and login functionality
  - Access-controlled blog creation/edit/update/delete

- 📝 **Blog Posts**

  - Auto-generated slugs and timestamped posts
  - Full CRUD operations (Create, Read, Update, Delete)
  - Users can edit/delete **only their own posts**
  - Superusers can manage **all posts**

- 📧 **Email Notifications**

  - Emails sent to authors on post **create**, **update**, and **delete**

- 📄 **Blog Pagination**

  - Paginated blog listing for better navigation through large content sets

- 💬 **Comment System**

  - Threaded comments and replies
  - Only authenticated users can comment

- 👑 **Admin Controls**

  - Superusers can edit/delete all posts
  - Regular users can only manage their own posts

- 🎨 **Bootstrap Styling**

  - Clean, responsive UI with alerts, forms, buttons, and modals

- 🔐 **.env-Based Email Settings**
  - Email configuration using environment variables via `django-environ`

---

## 🛠️ Tech Stack

- **Backend:** Django 5+
- **Frontend:** Bootstrap 5
- **Database:** SQLite (by default)

---

## 🔧 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/akashkhedekar8080/Inkwell.git
cd Inkwell
Create and activate virtual environment

bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Configure your environment variables

Create a .env file in the project root and add the following:

env
EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-app-password
Apply migrations

bash
python manage.py migrate
Create superuser (or use provided credentials)

bash
python manage.py createsuperuser
Or use default admin:

👤 Username: dell

🔑 Password: admin@123

Run the development server

bash
python manage.py runserver
Then open your browser:

cpp
http://127.0.0.1:8000/

📁 App Structure
graphql
Inkwell/
├── account/         # Login, Register views and templates
├── blogs/           # Blog models, views, templates
├── templates/       # All HTML templates (base, blogs, account)
├── static/          # CSS, JS, Bootstrap
├── manage.py
├── db.sqlite3

✍️ Author
Akash Khedekar
```
