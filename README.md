# 👥 Employee Management System

A clean, modern Employee Management dashboard built with vanilla HTML, CSS, and JavaScript — featuring smooth animations, real-time search/filter, and a polished UI inspired by modern SaaS dashboards.

🔗 **Live Demo:** [mauryashivi199-ui.github.io/employee-management-system](https://mauryashivi199-ui.github.io/employee-management-system/)

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

---

## 📌 Overview

This project simulates a real-world internal HR tool — letting an admin add, edit, search, filter, sort, and export employee records, all wrapped in a responsive, animated interface. It started as a Flask-based application and evolved into a fully client-side frontend deployable via GitHub Pages.

## ✨ Features

- **Add / Edit / Delete employees** with form validation and duplicate ID checks
- **Live search** across name, ID, and email
- **Department filter chips** with live counts
- **Sort** by name, department, or date joined
- **Color-coded avatars** generated per department for quick visual scanning
- **Export to CSV** — download the full employee list in one click
- **Animated stats dashboard** — total employees, departments, newest hire (count-up animation)
- **Toast notifications** for every action (add, update, delete)
- **Fully responsive** — works on mobile and desktop
- **Smooth micro-animations** — card entrances, modal transitions, hover states

## 🖼️ Preview

> Add a screenshot here once you have one — drag and drop an image into this section on GitHub, or use:
> `![App Screenshot](./screenshot.png)`

## 🛠️ Tech Stack

| Layer       | Technology                          |
|-------------|--------------------------------------|
| Frontend    | HTML5, CSS3, Vanilla JavaScript      |
| Fonts       | Space Grotesk, Inter, JetBrains Mono |
| Backend (optional) | Flask (Python)                |
| Containerization | Docker                          |
| Deployment  | GitHub Pages                         |

## 🚀 Getting Started

### Option 1 — View instantly (no setup)
Just open the live demo link above.

### Option 2 — Run locally (static)
```bash
git clone https://github.com/mauryashivi199-ui/employee-management-system.git
cd employee-management-system
# open index.html directly in your browser
```

### Option 3 — Run with Flask backend
```bash
pip install -r requirements.txt
python app.py
```

### Option 4 — Run with Docker
```bash
docker build -t employee-management-system .
docker run -p 5000:5000 employee-management-system
```

## 📂 Project Structure
