import os, sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from matcher import match_resume
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "portal.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = "supersecret"

# ------------------ Database ------------------
def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    # Resume table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS resumes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        section TEXT,
        score REAL,
        status TEXT DEFAULT 'pending'
    )""")
    # Admin account table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin_account(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )""")
    # Insert default admin if not exists
    cur.execute("SELECT * FROM admin_account WHERE username=?", ("admin",))
    if not cur.fetchone():
        cur.execute("INSERT INTO admin_account(username, password) VALUES (?,?)",
                    ("admin", generate_password_hash("admin123")))
    con.commit()
    con.close()

init_db()

# ------------------ Routes ------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method == "POST":
        file = request.files["resume"]
        if not file:
            flash("❌ No file selected", "danger")
            return redirect(url_for("upload"))

        # ✅ Only allow PDF files
        if not file.filename.lower().endswith(".pdf"):
            flash("❌ Only PDF resumes are accepted", "danger")
            return redirect(url_for("upload"))

        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_DIR, filename)
        file.save(path)

        section, score, matched_skills, missing_skills = match_resume(path)

        if section:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("INSERT INTO resumes(filename, section, score, status) VALUES (?,?,?,?)",
                        (filename, section, score, "pending"))
            con.commit()
            con.close()
            flash("✅ Resume uploaded successfully!", "success")
            return render_template("result.html", matched=True, section=section,
                                   score=score, matched_skills=matched_skills,
                                   missing_skills=missing_skills)
        else:
            flash("⚠ Your resume does not match. Suggestions shown below.", "danger")
            return render_template("result.html", matched=False, suggestions=missing_skills)

    return render_template("upload.html")


# ------------------ Admin Auth ------------------
@app.route("/admin", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("SELECT password FROM admin_account WHERE username=?", (user,))
        row = cur.fetchone()
        con.close()

        if row and check_password_hash(row[0], pw):
            session["admin"] = user
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials ❌", "danger")

    if "admin" in session:
        return redirect(url_for("dashboard"))
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    flash("✅ You have been logged out.", "success")
    return redirect(url_for("admin_login"))

@app.route("/admin/account", methods=["GET","POST"])
def admin_account():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        current_pw = request.form["current_password"]
        new_username = request.form.get("new_username")
        new_pw = request.form.get("new_password")

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("SELECT password FROM admin_account WHERE username=?", (session["admin"],))
        row = cur.fetchone()

        if row and check_password_hash(row[0], current_pw):
            # Change username if provided
            if new_username and new_username.strip():
                cur.execute("UPDATE admin_account SET username=? WHERE username=?",
                            (new_username.strip(), session["admin"]))
                session["admin"] = new_username.strip()

            # Change password if provided
            if new_pw and new_pw.strip():
                cur.execute("UPDATE admin_account SET password=? WHERE username=?",
                            (generate_password_hash(new_pw.strip()), session["admin"]))

            con.commit()
            flash("✅ Account updated successfully", "success")
        else:
            flash("❌ Current password is incorrect", "danger")
        con.close()

    return render_template("admin_account.html", username=session["admin"])

# ------------------ Dashboard ------------------
@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id, filename, section, score, status FROM resumes ORDER BY score DESC")
    resumes = cur.fetchall()
    con.close()

    sections = {}
    for r in resumes:
        resume_id, f, sec, sc, status = r
        sections.setdefault(sec, []).append((resume_id, f, sc, status))

    return render_template("admin.html", sections=sections)

@app.route("/select/<int:resume_id>")
def select_resume(resume_id):
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("UPDATE resumes SET status='selected' WHERE id=?", (resume_id,))
    con.commit()
    con.close()
    flash("Resume marked as Selected ✅", "success")
    return redirect(url_for("dashboard"))

@app.route("/download/resume/<filename>")
def download_resume(filename):
    if "admin" not in session:
        return redirect(url_for("admin_login"))
    path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        flash("File not found ❌", "danger")
        return redirect(url_for("dashboard"))

# ------------------ Downloads ------------------
@app.route("/download/pdf")
def download_pdf():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT filename, section, score, status FROM resumes ORDER BY section")
    data = cur.fetchall()
    con.close()

    pdf_path = os.path.join(BASE_DIR, "resumes_report.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height-50, "Resume Report")
    c.setFont("Helvetica", 12)

    y = height - 100
    for f, sec, sc, status in data:
        c.drawString(50, y, f"{f} | {sec} | {round(sc*100)}% | {status}")
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()

    return send_file(pdf_path, as_attachment=True)

@app.route("/download/excel")
def download_excel():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT filename, section, score, status FROM resumes", con)
    con.close()

    excel_path = os.path.join(BASE_DIR, "resumes_report.xlsx")
    df.to_excel(excel_path, index=False)

    return send_file(excel_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
