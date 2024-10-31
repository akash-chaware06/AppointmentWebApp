# WORK IN PROGRESS - NOT LINKED TO app.py COMPLETELY YET

from app import db
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin

Base = declarative_base()

class Appointment(Base):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    time_slot = db.Column(db.String(200), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    prof_id = db.Column(db.Integer, db.ForeignKey('professor.id'))

    student = db.relationship('Student', backref='appointments', lazy=True)
    professor = db.relationship('Professor', backref='appointments', lazy=True)


class Student(Base, UserMixin):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(10000), nullable=False)
    available_slots = db.Column(db.Integer, default=10)


class Professor(Base, UserMixin):
    __tablename__ = 'professor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(10000), nullable=False)
    available_slots = db.Column(db.Integer, default=10)

engine = create_engine('sqlite:///F:/RagineeAppointmentApp#3/database.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()