from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
conn = sqlite3.connect("feedback.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                s1 INTEGER,
                s2 INTEGER,
                s3 INTEGER,
                s4 INTEGER,
                s5 INTEGER,
                total INTEGER,
                percentage REAL,
                grade TEXT)''')
conn.commit()

# Home Page - Enter Marks
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

# Result Page
@app.route("/result", methods=["POST"])
def result():
    name = request.form["name"]
    s1 = int(request.form["s1"])
    s2 = int(request.form["s2"])
    s3 = int(request.form["s3"])
    s4 = int(request.form["s4"])
    s5 = int(request.form["s5"])

    total = s1 + s2 + s3 + s4 + s5
    percentage = round(total / 5, 2)

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B+"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    else:
        grade = "F"

    # Save to database
    c.execute("INSERT INTO students (name,s1,s2,s3,s4,s5,total,percentage,grade) VALUES (?,?,?,?,?,?,?,?,?)",
              (name, s1, s2, s3, s4, s5, total, percentage, grade))
    conn.commit()

    return render_template("result.html", name=name, s1=s1, s2=s2, s3=s3, s4=s4, s5=s5,
                           total=total, percentage=percentage, grade=grade)

# All Students Page
@app.route("/all")
def all_students():
    c.execute("SELECT * FROM students")
    rows = c.fetchall()

    students = []
    for row in rows:
        students.append({
            "name": row[1],
            "s1": row[2],
            "s2": row[3],
            "s3": row[4],
            "s4": row[5],
            "s5": row[6],
            "total": row[7],
            "percentage": row[8],
            "grade": row[9]
        })

    return render_template("all.html", students=students)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
