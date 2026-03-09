# Aegis | Campus Tutoring Platform

Aegis is a secure, role-based platform designed to bridge the gap between students needing help and peer mentors ready to teach.

This project uses a **Flask (Python)** backend and **Tailwind CSS (Node/npm)** for the frontend styling.

---

## 🛠️ Prerequisites

Before you start, make sure you have the following installed on your machine:

1. **Python 3.8+** (For the Flask backend)
2. **Node.js & npm** (For compiling Tailwind CSS)
3. **Git**

---

## 🚀 Setup Instructions

### 1. Clone the Repository

Pull the latest code to your local machine:

```bash
git clone <your-repo-link-here>
cd Aegis
```

### 2. Set Up the Python Backend

We use a virtual environment to keep our Python packages isolated.

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables (Mailtrap)

Aegis uses **Mailtrap** to safely test sending OTP emails without spamming real inboxes. You will need your own free Mailtrap account to receive the OTPs locally.

1. Go to [Mailtrap.io](https://mailtrap.io/) and create a free account.
2. Go to **Email Testing > Inboxes**, find your SMTP credentials, and copy your Username and Password.
3. In the root folder of this project, duplicate the `.env.example` file and rename the new file to exactly `.env`.
4. Open your new `.env` file and paste your credentials:

```env
MAILTRAP_USERNAME=your_username_here
MAILTRAP_PASSWORD=your_password_here
```

_(Note: The `.env` file is ignored by Git, so your credentials will stay secure on your machine)._

### 4. Set Up the Frontend (Tailwind CSS)

We use npm to manage our CSS compilation. First, install the Node dependencies:

```bash
npm install
```

To compile the Tailwind CSS so the UI looks correct, run:

```bash
npm run dev:css
```

---

## 🏃‍♂️ Running the Application

Make sure your virtual environment is activated, then start the Flask development server:

```bash
python app.py
```

Open your browser and navigate to: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Test Accounts

The database automatically seeds mock accounts when the server starts. You can use these credentials to test the platform.

**Student Account (Redirects to Student Dashboard):**

- **Email:** `22012345@student.dut4life.ac.za`
- **Password:** `password123`

**Mentor Account (Redirects to Mentor Dashboard):**

- **Email:** `alex@dut.ac.za`
- **Password:** `admin`

_(When you log in, check your personal Mailtrap inbox for the OTP code!)_
