"""
HealinBelieve — Database Models
All SQLAlchemy models for the medical tourism platform.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Patient, Hospital, or Admin user."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='patient')  # patient | hospital | admin
    phone = db.Column(db.String(30))
    country = db.Column(db.String(60))
    language = db.Column(db.String(10), default='en')
    avatar = db.Column(db.String(256))
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy=True, foreign_keys='Appointment.patient_id')
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy=True)
    messages_sent = db.relationship('Message', backref='sender', lazy=True, foreign_keys='Message.sender_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Hospital(db.Model):
    """Hospital / Medical facility."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    country = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    website = db.Column(db.String(200))
    image = db.Column(db.String(256))
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    specialties = db.Column(db.Text)  # JSON string
    accreditations = db.Column(db.Text)  # JSON string
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('hospital_profile', cascade='all, delete-orphan'))
    doctors = db.relationship('Doctor', backref='hospital', lazy=True, cascade='all, delete-orphan')
    treatments = db.relationship('Treatment', backref='hospital', lazy=True, cascade='all, delete-orphan')
    packages = db.relationship('Package', backref='hospital', lazy=True, cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='hospital', lazy=True, cascade='all, delete-orphan')


class Doctor(db.Model):
    """Doctor profile linked to a hospital."""
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(80), nullable=False)
    qualifications = db.Column(db.Text)
    experience_years = db.Column(db.Integer, default=0)
    bio = db.Column(db.Text)
    image = db.Column(db.String(256))
    languages = db.Column(db.Text)  # JSON string
    consultation_fee = db.Column(db.Float, default=0)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Treatment(db.Model):
    """Medical treatment offered by a hospital."""
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=False)  # e.g. Cardiac, Dental, Cosmetic
    description = db.Column(db.Text)
    min_cost = db.Column(db.Float, default=0)
    max_cost = db.Column(db.Float, default=0)
    duration_days = db.Column(db.Integer, default=1)
    success_rate = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Package(db.Model):
    """Medical tourism package including treatment + travel services."""
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    treatment_name = db.Column(db.String(150))
    includes_hotel = db.Column(db.Boolean, default=False)
    includes_airport_pickup = db.Column(db.Boolean, default=False)
    includes_translator = db.Column(db.Boolean, default=False)
    includes_post_care = db.Column(db.Boolean, default=False)
    hotel_details = db.Column(db.String(256))
    price = db.Column(db.Float, default=0)
    duration_days = db.Column(db.Integer, default=7)
    image = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Appointment(db.Model):
    """Booking / appointment between patient and hospital."""
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    treatment_name = db.Column(db.String(150))
    preferred_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending | confirmed | rejected | completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship('Doctor', backref='appointments')


class MedicalRecord(db.Model):
    """Patient-uploaded medical records."""
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(256), nullable=False)
    original_name = db.Column(db.String(256))
    file_type = db.Column(db.String(20))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class Message(db.Model):
    """Simple messaging between patient and hospital."""
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    hospital_id = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Review(db.Model):
    """Patient review for a hospital."""
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient_user = db.relationship('User', backref='reviews')
    hospital_ref = db.relationship('Hospital', backref='reviews')
