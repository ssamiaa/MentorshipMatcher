
# 🎓 Learning Hub – Mentorship and Course Platform

**Learning Hub** is a modern web platform built with **Python + Flask** that connects learners and mentors through skill-based teaching, course creation, and peer-to-peer exchanges. Whether you want to teach, learn, or do both, this platform offers a simple and interactive space to register, match, and enroll in courses.

---

## 🌟 Features

### 🔐 User Authentication

* Simple **sign-up** and **login** system
* Session-based login using Flask sessions

### 🧑‍🏫 Skills & Matching

* Users can add **skills they can teach** and **skills they want to learn**
* Based on this, the platform shows **learning matches**
* Users can engage in **mutual skill exchange** or choose to enroll in paid courses

### 📚 Course Management

* Users who have added a “teach” skill can **create courses**
* Courses can be **free** or **paid**
* Instructors define title, description, price, start date, and if they accept skill exchanges

### 🛒 Course Enrollment

* Students can **browse all available courses**
* Can **enroll** using a **fake but realistic payment flow**:

  * Choose payment method (Visa, MasterCard, Google Pay, Paytm)
  * Input dummy payment details depending on the selected method
* Instructors **cannot enroll** in their own courses
* Already enrolled users see a “You’re already enrolled” message

### 💬 Help Page

* Guides new users on how the platform works:

  * How to add skills
  * How course creation works
  * How skill exchange can waive payment
  * How to enroll and see your dashboard

---

## 📂 File Structure Overview

```bash
├── flask/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── dashboard.html
│   │   ├── create_course.html
│   │   ├── browse_courses.html
│   │   ├── enroll.html
│   │   └── help.html
│   ├── static/ (optional for CSS/images)
│
├── models.py
├── matcher.py
├── app.py
└── mentorship.db (SQLite database)
```

---

## 🛠️ Tech Stack

* **Backend**: Python 3, Flask
* **Database**: SQLite3
* **Frontend**: HTML5, CSS3 (with inline styles), Jinja2 templates
* **Other**: Bootstrap/Tailwind-ready layout, Sessions, Flash messages

---

## 🧪 How to Run Locally

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/learning-hub.git
   cd learning-hub
   ```

2. **Set up a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install Flask
   ```

4. **Run the app**:

   ```bash
   python app.py
   ```

5. Open your browser and go to `http://localhost:5000`

---

## 🔮 Future Improvements

* Add profile images and bio for mentors
* Add chat or scheduling functionality
* Enable filtering or search in course browsing
* Admin panel for managing users and reports
* Email notifications for new matches or enrollments

---

## 💡 Sample Use Case

> A user named Samia signs up and adds “Python” as a teaching skill and “UI/UX” as a learning skill.
> Another user, Arjun, teaches UI/UX and wants to learn Python.
> They are matched on the dashboard.
> Samia also creates a course called “Intro to Python” that Arjun can enroll in either by paying or exchanging a skill.

---

## 🧑‍💻 Developer

**Samia Sajid**
Built as a side project to explore real-world applications of Flask, web development, and interactive learning platforms.

---

Let me know if you'd like it styled with Markdown badges or deployment instructions (e.g., for Render or Replit).
