from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# -----------------------------
# MongoDB Connection
# -----------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["online_exam"]

students = db["students"]

# -----------------------------
# Home Page
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -----------------------------
# Student Registration
# -----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        rollno = request.form['rollno']
        password = request.form['password']

        # Check if email already exists
        existing_user = students.find_one({"email": email})

        if existing_user:
            return "Email already registered!"

        students.insert_one({
            "fullname": fullname,
            "email": email,
            "rollno": rollno,
            "password": password
        })

        return redirect(url_for('login'))

    return render_template('register.html')


# -----------------------------
# Student Login
# -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = students.find_one({
            "email": email,
            "password": password
        })

        if user:
            return render_template(
                "dashboard.html",
                name=user["fullname"],
                rollno=user["rollno"]
            )

        return "Invalid Email or Password"

    return render_template("login.html")


# -----------------------------
# Dashboard
# -----------------------------
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# -----------------------------
# Exam Page
# -----------------------------
@app.route('/exam')
def exam():
    return render_template("exam.html")


# -----------------------------
# Result Page
# -----------------------------
@app.route('/result')
def result():
    return render_template("result.html", name="Student")


# -----------------------------
# Logout
# -----------------------------
@app.route('/logout')
def logout():
    return redirect(url_for('home'))


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
if __name__ == "__main__":
  @app.route('/admin_login')
  def admin_login():
    return render_template('admin_login.html')


  @app.route('/admin_dashboard')
  def admin_dashboard():
    return render_template('admin_dashboard.html')