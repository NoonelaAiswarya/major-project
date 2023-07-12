from datetime import date
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
db= sqlite3.connect('course_enrollment.db', check_same_thread=False)

cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        age INTEGER,
        gender TEXT,
        course_id INTEGER,
        enrolled_date DATE,
        email TEXT,
        ph_no TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        capacity INTEGER
    )
''')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_enroll', methods=["POST", "GET"])
def new_enroll():
    if request.method == "POST":
        # Code for adding a new enrollment
        student_name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        course_id = request.form.get("course_id")
        enrolled_date = date.today().strftime("%Y-%m-%d")
        email = request.form.get("email")
        ph_no = request.form.get("phone")
        
        query = "INSERT INTO enrollments (student_name, age, gender, course_id, enrolled_date, email, ph_no) VALUES (?, ?, ?, ?, ?, ?, ?)"
        values = (student_name, age, gender, course_id, enrolled_date, email, ph_no)
        cursor.execute(query, values)
        db.commit()
        
        decrease_capacity_query = "UPDATE courses SET capacity = capacity - 1 WHERE course_id = ? AND capacity > 0"
        decrease_capacity_values = (course_id,)
        cursor.execute(decrease_capacity_query, decrease_capacity_values)
        db.commit()
        
        return redirect('/new_enroll')
    else:
        courses = get_courses()
        return render_template('new_enroll.html', courses=courses)


def get_courses():
    query = "SELECT * FROM courses"
    cursor.execute(query)
    return cursor.fetchall()

@app.route('/course')
def view_courses():
    courses = get_courses()
    return render_template('course.html', courses=courses)

@app.route('/course/remove', methods=['POST'])
def remove_course():
    course_id = request.form['course_id']
    query = "DELETE FROM courses WHERE course_id = %s"
    values = (course_id,)
    cursor.execute(query, values)
    db.commit()
    return redirect('/course')

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['course_name']
        capacity = request.form['capacity']
        
        query = "INSERT INTO courses (course_name, capacity) VALUES (?, ?)"
        values = (course_name, capacity)
        cursor.execute(query, values)
        db.commit()
        
        return redirect('/course')
    else:
        return render_template('add_course.html')



def get_enrolls():
    query = "SELECT * FROM enrollments"
    cursor.execute(query)
    return cursor.fetchall()

@app.route('/enroll')
def view_enrolls():
    enrolls = get_enrolls()
    return render_template('enroll.html', enrollments=enrolls)

@app.route('/enroll/remove', methods=['POST'])
def remove_enroll():
    enrollment_id = request.form['enrollment_id']
    query = "DELETE FROM enrollments WHERE enrollment_id = %s"
    values = (enrollment_id,)
    cursor.execute(query, values)
    db.commit()
    return redirect('/enroll')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
