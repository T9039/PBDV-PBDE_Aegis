# Aegis | Campus Tutoring Platform

Aegis is a secure, role-based platform designed to bridge the gap between students needing help and peer mentors ready to teach.

This project uses a **Flask (Python)** backend, **MariaDB/MySQL** for the database, and **Tailwind CSS (Node/npm)** for the frontend styling.

---

## 🛠️ Prerequisites

Before you start, make sure you have the following installed on your machine:

1. **Python 3.8+** (For the Flask backend)
2. **Node.js & npm** (For compiling Tailwind CSS)
3. **MariaDB or MySQL** (For the local database)
4. **Git**

---

## 🚀 Setup Instructions

### 1. Clone the Repository

Pull the latest code to your local machine:

```bash
git clone [https://github.com/T9039/PBDV-PBDE_Aegis.git](https://github.com/T9039/PBDV-PBDE_Aegis.git)
cd Aegis
```

### 2. Set Up the Python Backend

We use a virtual environment to keep our Python packages isolated.

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up the Local Database (MariaDB/MySQL)

Aegis uses a local relational database for development. You need to create the database and a dedicated app user on your machine.

**Linux/Mac:**
First, ensure the database service is running in the background:

- **Linux:** `sudo systemctl start mariadb` (or `mysql`)
- **Mac (Homebrew):** `brew services start mariadb` (or `mysql`)

Then, log into your local database terminal as root:

```bash
sudo mariadb
```

**Windows:**
The service usually starts automatically. Open the **MySQL/MariaDB Command Line Client** from your Start menu, or open your terminal and run:

```cmd
mysql -u root -p
```

**Once logged into the database prompt, run these exact SQL commands:**
_(Feel free to change `your_secure_db_password` to whatever you want)_

```sql
CREATE DATABASE IF NOT EXISTS aegis_db;
CREATE USER 'aegis_app_user'@'localhost' IDENTIFIED BY 'your_secure_db_password';
GRANT ALL PRIVILEGES ON aegis_db.* TO 'aegis_app_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Configure Environment Variables

Aegis needs environment variables to connect to your local database and to Mailtrap (for OTP emails).

1. In the root folder, duplicate `.env.example` and rename it to exactly `.env`.
2. Open your new `.env` file and configure your credentials:

```env
# Mailtrap Credentials (Get these from your free Mailtrap.io inbox)
MAILTRAP_USERNAME=your_mailtrap_username
MAILTRAP_PASSWORD=your_mailtrap_password

# Database Credentials
# Format: mysql+pymysql://username:password@localhost:3306/database_name
DATABASE_URL=mysql+pymysql://aegis_app_user:your_secure_db_password@localhost:3306/aegis_db
```

### 5. Set Up the Frontend (Tailwind CSS)

We use npm to manage our CSS compilation. First, install the Node dependencies:

```bash
npm install
```

To compile the Tailwind CSS so the UI looks correct, open a second terminal and run:

```bash
npm run dev:css
```

---

## 🌱 Seeding the Database

Because everyone runs their own local database, yours is currently empty! We have a script that automatically builds the tables and injects mock users so you can test the app immediately.

Make sure your Python virtual environment is active, then run:

```bash
python seed.py
```

_(You can run this command anytime you want to wipe your database and start fresh with the mock data!)_

---

## 🏃‍♂️ Running the Application

With your database seeded and environment active, start the Flask development server:

```bash
python app.py
```

Open your browser and navigate to: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Test Accounts

Running `seed.py` creates several test accounts. Here are the main two you can use to test the different dashboards:

**Student Account (Redirects to Student Dashboard):**

- **Email:** `22012345@dut4life.ac.za`
- **Password:** `password123`

**Staff/Mentor Account (Redirects to Mentor Dashboard):**

- **Email:** `alex@dut.ac.za`
- **Password:** `admin`

_(When you log in, remember to check your personal Mailtrap inbox for the OTP code!)_
