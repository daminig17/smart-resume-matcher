# smart-resume-matcher
A Flask + SQLite based resume screening system with rule-based skill matching, missing skill suggestions, and admin dashboard.

---

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

