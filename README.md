# Mentorship Matching CLI Application

## Overview

This is a **Command-Line Interface (CLI) application** for managing a mentorship matching platform.
It allows users to register, declare skills they can teach or want to learn, and automatically find matching pairs based on skill compatibility.

The application uses **SQLite** as a lightweight, file-based database and is implemented in **Python**.

---

## Who Will Use It

This tool is designed for:

* **Students** seeking peer mentorship in different subjects or technologies
* **Volunteers and instructors** who want to offer skills training
* **Community organizations, clubs, or educational programs** that need a simple way to match mentors and mentees

Potential use cases include:

* University coding clubs
* Non-profits providing tutoring
* Internal training programs for small teams

Because it is CLI-based and local, it’s best suited for small-to-medium groups who don’t need a web interface.

---

## Features

* **User Registration and Login**

  * Sign up with a name and email address (email must be unique)
  * Log in to an existing account
* **Skill Management**

  * Add skills you can *teach* or *learn*
  * View your skills
* **Matching**

  * Automatically generate matches based on:

    * You can teach a skill someone else wants to learn
    * You want to learn a skill someone else can teach
  * View your matched users, including the matching score (number of overlapping skills)
* **Persistent Storage**

  * All data is stored in `mentorship.db` SQLite file

---

## How Matching Works

* When you add a skill:

  * The system searches for other users with complementary skills
  * If a compatible pairing exists (e.g., you want to learn Python and someone else teaches it), it generates a match
  * The match is stored with a *score*, indicating how many skill overlaps you have
* Each unique user pair appears only once, regardless of who added the skill first

---

## How to Use

1. Run the application:

   ```bash
   python3 main.py
   ```
2. Sign up or log in.
3. Add skills you can teach or learn.
4. View your skills or matches.
5. Continue adding new skills to expand matching opportunities.

---

## Possible Improvements and Extensions

This project provides a solid starting point but can be extended further:

* **Web Interface**

  * Build a web frontend (e.g., Flask or Django) to replace CLI.
* **Notifications**

  * Email users when new matches are found.
* **Skill Levels**

  * Allow specifying proficiency (beginner, intermediate, expert).
* **Match Acceptance**

  * Let users accept or decline matches.
* **Messaging**

  * Implement a basic communication system between matched users.
* **Admin Dashboard**

  * Provide admin tools to view all users, skills, and matches.
* **Analytics**

  * Show statistics about popular skills and match activity.
* **Authentication**

  * Add password-based login instead of only email-based identification.
* **Recurring Events**

  * Allow scheduling mentorship sessions.

---

## Technology Stack

* Python 3
* SQLite (via `sqlite3` module)

---

## Getting Started

1. Clone the repository:

   ```bash
   git clone <repo-url>
   ```
2. Install Python 3 if not already installed.
3. Run:

   ```bash
   python3 main.py
   ```
4. Follow on-screen prompts.

---

If you’d like, I can help you format this for Markdown, or tailor it further for your specific context.
