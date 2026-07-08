## ⚙️ Setup and Installation

Follow these steps to set up the application locally:

### 1. Clone the Repository
```bash
git clone https://github.com/hetmehta189/Blog-Website.git
cd Blog-Website
```

### 2. Create and Activate a Virtual Environment
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the File Upload Directory
The directory for user-uploaded files is gitignored and must be created manually before uploading files:
```bash
mkdir static/files
```

### 5. Setup Configuration
Copy `config.json.example` to create `config.json`:
```bash
cp config.json.example config.json
```

Open `config.json` and configure the following parameters:
```json
{
  "params": {
    "blog_name": "My Blog",
    "blog_subheading": "A place where I share my thoughts",
    "about_text": "Hello! I am a passionate blogger...",
    "upload_location": "static/files",
    "gmail_user": "your-email@gmail.com",
    "gmail_password": "your-gmail-app-password",
    "local_uri": "mysql+pymysql://root:@localhost/blog_db",
    "prod_uri": "mysql+pymysql://production_user:password@production_host/blog_db",
    "no_of_posts": 5,
    "admin_user": "admin",
    "admin_password": "secure_admin_password",
    "wa_url": "https://wa.me/1234567890",
    "insta_url": "https://instagram.com/yourusername",
    "gh_url": "https://github.com/yourusername"
  }
}
```
> 💡 **Tip:** If you are using Gmail SMTP for notification emails, you must configure a **Gmail App Password** rather than your main account password.

---

## 🗄️ Database Setup

This project uses SQLAlchemy. The models support any relational database compatible with SQLAlchemy (e.g., MySQL, SQLite, PostgreSQL).

### Table Schema

#### 1. `posts` Table (Blog Articles)
| Column Name | Data Type | Modifiers | Description |
| :--- | :--- | :--- | :--- |
| `srno` | `Integer` | Primary Key, Auto-increment | Unique identifier |
| `title` | `String(100)` | Nullable=False | Title of the blog post |
| `slug` | `String(100)` | Nullable=False | URL-friendly slug path |
| `tagline` | `String(100)` | Nullable=False | Subtitle or tagline |
| `content` | `Text` | Nullable=False | Main post body content |
| `img_file` | `String(255)` | Nullable=True | Image filename used in header |
| `date_of_post`| `DateTime` | Default=Current UTC time | Time of post creation |

#### 2. `contacts` Table (Form Submissions)
| Column Name | Data Type | Modifiers | Description |
| :--- | :--- | :--- | :--- |
| `srno` | `Integer` | Primary Key, Auto-increment | Unique identifier |
| `name_of_person`| `Text` | Nullable=False | Sender's full name |
| `email` | `String(100)` | Nullable=False | Sender's email address |
| `phone_number` | `String(20)` | Nullable=True | Sender's phone number |
| `message` | `Text` | Nullable=False | Feedback or query message |
| `Date_of_contact`| `DateTime` | Default=Current UTC time | Timestamp of submission |

### 🛠️ Automatically Create Tables
Before starting the app, you can automatically create the tables inside your database (configured in `config.json`) using this command:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

## 🏃 Running the Application

Once configuration and database setup are done, execute the main entrypoint:
```bash
python app.py
```
By default, the server will start in debug mode on **`http://127.0.0.1:5000/`**.

* **Homepage**: `http://127.0.0.1:5000/`
* **Admin Dashboard**: `http://127.0.0.1:5000/dashboard`
```
