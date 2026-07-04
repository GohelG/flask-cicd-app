from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import certifi
import os

# Load env vars from .env file
load_dotenv()

app = Flask(__name__)

# Set configurations (using MONGO_URI uniformly)
app.config["MONGO_URI"] = os.getenv("MONGO_URI") or os.getenv("MONGO_URL") or "mongodb://localhost:27017/student_db"
app.secret_key = os.getenv("SECRET_KEY", "default_fallback_secret_key")

# Instantiate PyMongo globally
mongo = PyMongo()

# Initialize conditionally to support BOTH local tests and production Atlas SSL
if "localhost" in app.config["MONGO_URI"] or "127.0.0.1" in app.config["MONGO_URI"]:
    # Local development/testing: No SSL configuration required
    mongo.init_app(app)
else:
    # Production Atlas/Remote Cluster: Secure TLS connection mandatory
    mongo.init_app(app, tlsCAFile=certifi.where())

# Home page -> list students
@app.route('/')
def index():
    students = mongo.db.students.find()
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        mongo.db.students.insert_one({
            "name": name,
            "email": email,
            "course": course
        })
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Update student
@app.route('/update/<student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
    if request.method == 'POST':
        new_name = request.form['name']
        new_email = request.form['email']
        new_course = request.form['course']
        mongo.db.students.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": {"name": new_name, "email": new_email, "course": new_course}}
        )
        return redirect(url_for('index'))
    return render_template('update_student.html', student=student)

# Delete student
@app.route('/delete/<student_id>')
def delete_student(student_id):
    mongo.db.students.delete_one({"_id": ObjectId(student_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
