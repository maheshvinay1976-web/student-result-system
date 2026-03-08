from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    sub1 INTEGER,
    sub2 INTEGER,
    sub3 INTEGER,
    sub4 INTEGER,
    sub5 INTEGER,
    total INTEGER,
    percentage REAL,
    grade TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# Grade calculation
def calculate_grade(p):
    if p >= 90:
        return "A"
    elif p >= 75:
        return "B"
    elif p >= 50:
        return "C"
    else:
        return "Fail"


# Home page
@app.route("/")
def index():
    return render_template("index.html")


# Result calculation
@app.route("/result", methods=["POST"])
def result():

    name = request.form["name"]

    s1 = int(request.form["s1"])
    s2 = int(request.form["s2"])
    s3 = int(request.form["s3"])
    s4 = int(request.form["s4"])
    s5 = int(request.form["s5"])

    total = s1 + s2 + s3 + s4 + s5
    percentage = total / 5
    grade = calculate_grade(percentage)

    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute(
    "INSERT INTO results(name,sub1,sub2,sub3,sub4,sub5,total,percentage,grade) VALUES(?,?,?,?,?,?,?,?,?)",
    (name,s1,s2,s3,s4,s5,total,percentage,grade)
    )

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        name=name,
        total=total,
        percentage=percentage,
        grade=grade
    )


# Show all students
@app.route("/all")
def all_results():

    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM results")
    data = cur.fetchall()

    conn.close()

    return render_template("all.html", data=data)


app.run(host="0.0.0.0", port=5000)
