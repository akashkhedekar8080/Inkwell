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
- 💬 **Comment System**
  - Threaded comments and replies
  - Only authenticated users can comment
- 👑 **Admin Controls**
  - Superusers can edit/delete all posts
  - Regular users can only manage their own posts
- 🎨 **Bootstrap Styling**
  - Clean, responsive UI with alerts, forms, buttons, and modals

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
Visit the app in browser
http://127.0.0.1:8000/

📁 App Structure
graphql
Copy
Edit
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
