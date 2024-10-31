from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from db import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i want to die.'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///F:/RagineeAppointmentApp#3/database.db'

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

professors = [
    {"name": "One"},
    {"name": "Two"},
    {"name": "Three"},
    {"name": "Four"},
    {"name": "Five"},
    {"name": "Six"},
    {"name": "Seven"},
    {"name": "Eight"},
    {"name": "Nine"},
    {"name": "Ten"},
]

time_slots = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "13:00", "13:30", "14:00"]

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Professor).get(user_id) or db.session.query(Student).get(user_id)

@app.route('/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')

    profession = request.form.get('profession_select')
    email = request.form.get('email')
    name = str(request.form.get('fName') + request.form.get('lName'))
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    
    existing_user = None

    if not email:
        flash('Please Enter an Email.', category='error')
    elif profession == 'professor':
        existing_user = db.session.query(Professor).filter_by(email=email).first()
    else:
        existing_user = db.session.query(Student).filter_by(email=email).first()

    if existing_user:
        flash('Email already exists. Please login instead.', category='error')
        return redirect(url_for('login'))
    elif not name:
        flash('Please Enter a name.', category='error')
    elif not password1 or not password2:
        flash('Please Enter a password.', category='error')
    elif password1 != password2:
        flash("Passwords don't match.", category='error')
    else:
        if profession == 'professor':
            new_account = Professor(name=name, email=email, password=generate_password_hash(password1))
        else:
            new_account = Student(name=name, email=email, password=generate_password_hash(password1))

        db.session.add(new_account)
        db.session.commit()
        login_user(new_account)
        flash('Sign up successful! Account Created.', category='success')
        return redirect(url_for('login'))

    return redirect(url_for('sign_up'))
            
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    profession = request.form.get('profession_select')
    email = request.form.get('email')
    password = request.form.get('password1')

    if profession == 'student':
        user = db.session.query(Student).filter_by(email=email).first()
    else:
        user = db.session.query(Professor).filter_by(email=email).first()

    if user is None:
        flash('Email does not exist. Please sign up.', category='error')
        return redirect(url_for('sign_up'))

    if not check_password_hash(user.password, password):  
        flash('Incorrect password. Please try again.', category='error')
        return redirect(url_for('login'))

    login_user(user)
    flash('Logged in Successfully.', category='success')
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html', professors=professors)

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')

@app.route('/book/<prof_name>', methods=['GET', 'POST'])
def book(prof_name):
    if request.method == 'POST':
        student_name = request.form['student_name']
        time_slot = request.form['time_slot']
        new_appointment = Appointment(student_name, prof_name, time_slot)
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('confirmation', prof_name=prof_name, student_name=student_name, time_slot=time_slot))
    return render_template('book.html', professor=next((p for p in professors if p['name'] == prof_name), None), time_slots=time_slots)

@app.route('/confirmation')
def confirmation():
    student_name = request.args.get('student_name')
    time_slot = request.args.get('time_slot')
    prof_name = request.args.get('prof_name')
    professor = next((p for p in professors if p['name'] == str(prof_name)), None)
    return render_template('confirmation.html', student_name=student_name, time_slot=time_slot, professor=professor)

if __name__ == '__main__':
    app.run(debug=True)
