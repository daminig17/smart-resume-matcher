# 📄 Smart Resume Matcher (Rule-Based)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/) 
[![Flask](https://img.shields.io/badge/Flask-2.0-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/) 
[![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)  
[![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red.svg)]()

A Flask + SQLite based resume screening system with rule-based skill matching, missing skill suggestions, and admin dashboard.

---<img width="800" height="800" alt="Resume Matching System Workflow" src="https://github.com/user-attachments/assets/911d1838-6559-4b34-bf72-4b308903fcd8" />


## 🚀 Features
- 🎨 **Attractive Landing Page** with animations and navigation bar.
- 📤 **Resume Upload (PDF only)** – Candidates upload their resumes.
- 🧠 **Rule-Based Matching** – Extracts skills and compares with predefined IT sector requirements.
- 📊 **Result Page** – Shows:
  - ✅ Matched Skills
  - ❌ Missing Skills
  - 📈 Confidence Score (progress bar + Chart.js visualization)
- 👨‍💼 **Admin Dashboard** – 
  - View all uploaded resumes
  - See matched sectors & scores
  - Download resumes
  - Export reports in **PDF/Excel**
  - Update **Admin Username/Password**
- 🔒 **Security** –
  - Admin passwords hashed with `werkzeug.security`
  - Session-based login
  - File upload restricted to **PDF only**
- 📱 Responsive, modern UI with animations & toasts.

---

## 🛠️ Tech Stack

**Frontend:**
- HTML5, CSS3 (custom animations)
- JavaScript, Chart.js (data visualization)

**Backend:**
- Python (Flask)
- Jinja2 Templating

**Database:**
- SQLite (lightweight, file-based)

**Libraries:**
- Flask – Web framework
- Pandas – Excel/CSV handling
- ReportLab – PDF generation
- PyPDF2 – Resume text extraction
- Werkzeug – Password hashing
- Chart.js – Charts & graphs

---

## 📂 Project Structure

## Screenshot
<img width="600" height="400" alt="interfaces" src="https://github.com/user-attachments/assets/e1632a06-e3d2-4353-bf10-f0211d49b293" />

## 🔮 Future Improvements

🔹 Extend to a Machine Learning (ML/NLP) version with BERT embeddings

🔹 Add Job Recommendation Ranking

🔹 Deploy on Heroku/Render/AWS for live access

