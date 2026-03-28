"""
HealinBelieve — Medical Tourism Platform
Main Flask application with all routes.
"""

import os, json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User, Hospital, Doctor, Treatment, Package, Appointment, MedicalRecord, Message, Review
from seed import seed_database
from matching_engine import calculate_match_scores

# ─── App Config ──────────────────────────────────────────────────
app = Flask(__name__)
app.config['SECRET_KEY'] = 'healinbelieve-secret-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healinbelieve.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ─── Template Helpers ────────────────────────────────────────────
@app.template_filter('from_json')
def from_json_filter(value):
    try:
        return json.loads(value) if value else []
    except Exception:
        return []


@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.utcnow().year,
        'languages': {'en': 'English', 'es': 'Español', 'ar': 'العربية', 'zh': '中文', 'hi': 'हिन्दी', 'de': 'Deutsch', 'fr': 'Français', 'ko': '한국어', 'th': 'ไทย', 'tr': 'Türkçe'},
    }


# ═════════════════════════════════════════════════════════════════
#  PUBLIC PAGES
# ═════════════════════════════════════════════════════════════════

@app.route('/')
def home():
    hospitals = Hospital.query.filter_by(is_approved=True).all()
    doctors = Doctor.query.filter_by(is_active=True).limit(6).all()
    packages = Package.query.filter_by(is_active=True).limit(3).all()
    stats = {
        'hospitals': Hospital.query.filter_by(is_approved=True).count(),
        'doctors': Doctor.query.filter_by(is_active=True).count(),
        'countries': db.session.query(Hospital.country).distinct().count(),
        'treatments': Treatment.query.filter_by(is_active=True).count(),
    }
    return render_template('index.html', hospitals=hospitals, doctors=doctors, packages=packages, stats=stats)


@app.route('/hospitals')
def hospital_list():
    country = request.args.get('country', '')
    specialty = request.args.get('specialty', '')
    q = Hospital.query.filter_by(is_approved=True)
    if country:
        q = q.filter(Hospital.country == country)
    if specialty:
        q = q.filter(Hospital.specialties.contains(specialty))
    hospitals = q.all()
    countries = [r[0] for r in db.session.query(Hospital.country).distinct().all()]
    return render_template('hospitals.html', hospitals=hospitals, countries=countries, selected_country=country, selected_specialty=specialty)


@app.route('/hospital/<int:hospital_id>')
def hospital_detail(hospital_id):
    hospital = db.session.get(Hospital, hospital_id) or abort(404)
    return render_template('hospital_detail.html', hospital=hospital)


@app.route('/doctors')
def doctor_list():
    specialty = request.args.get('specialty', '')
    q = Doctor.query.filter_by(is_active=True)
    if specialty:
        q = q.filter(Doctor.specialty == specialty)
    doctors = q.all()
    specialties = [r[0] for r in db.session.query(Doctor.specialty).distinct().all()]
    return render_template('doctors.html', doctors=doctors, specialties=specialties, selected_specialty=specialty)


@app.route('/treatments')
def treatment_search():
    category = request.args.get('category', '')
    country = request.args.get('country', '')
    max_price = request.args.get('max_price', '')
    q = Treatment.query.filter_by(is_active=True)
    if category:
        q = q.filter(Treatment.category == category)
    if country:
        q = q.join(Hospital).filter(Hospital.country == country)
    if max_price:
        q = q.filter(Treatment.min_cost <= float(max_price))
    treatments = q.all()
    categories = [r[0] for r in db.session.query(Treatment.category).distinct().all()]
    countries = [r[0] for r in db.session.query(Hospital.country).distinct().all()]
    return render_template('treatments.html', treatments=treatments, categories=categories, countries=countries,
                           selected_category=category, selected_country=country, selected_max_price=max_price)


@app.route('/packages')
def package_list():
    packages = Package.query.filter_by(is_active=True).all()
    return render_template('packages.html', packages=packages)


@app.route('/compare')
def cost_compare():
    treatments = Treatment.query.filter_by(is_active=True).all()
    categories = [r[0] for r in db.session.query(Treatment.category).distinct().all()]
    return render_template('compare.html', treatments=treatments, categories=categories)


# ─── Content Pages ───────────────────────────────────────────────
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/visa-info')
def visa_info():
    return render_template('visa_info.html')

@app.route('/travel-guide')
def travel_guide():
    return render_template('travel_guide.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


# ═════════════════════════════════════════════════════════════════
#  AUTHENTICATION
# ═════════════════════════════════════════════════════════════════

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'patient')
        country = request.form.get('country', '')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))

        user = User(name=name, email=email, role=role, country=country)
        user.set_password(password)
        if role == 'hospital':
            user.is_approved = False
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Welcome to HealinBelieve!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(request.args.get('next') or url_for('dashboard'))
        flash('Invalid email or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# ═════════════════════════════════════════════════════════════════
#  DASHBOARDS
# ═════════════════════════════════════════════════════════════════

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'hospital':
        return redirect(url_for('hospital_dashboard'))
    return redirect(url_for('patient_dashboard'))


# ─── Patient Dashboard ──────────────────────────────────────────
@app.route('/patient/dashboard')
@login_required
def patient_dashboard():
    appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.created_at.desc()).all()
    records = MedicalRecord.query.filter_by(patient_id=current_user.id).order_by(MedicalRecord.uploaded_at.desc()).all()
    messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).limit(20).all()
    return render_template('patient_dashboard.html', appointments=appointments, records=records, messages=messages)


@app.route('/patient/book', methods=['POST'])
@login_required
def book_appointment():
    hospital_id = request.form.get('hospital_id')
    doctor_id = request.form.get('doctor_id')
    treatment_name = request.form.get('treatment_name', '')
    preferred_date = request.form.get('preferred_date')
    notes = request.form.get('notes', '')

    appt = Appointment(
        patient_id=current_user.id,
        hospital_id=hospital_id,
        doctor_id=doctor_id if doctor_id else None,
        treatment_name=treatment_name,
        preferred_date=datetime.strptime(preferred_date, '%Y-%m-%d').date() if preferred_date else None,
        notes=notes,
    )
    db.session.add(appt)
    db.session.commit()
    flash('Appointment booked successfully! The hospital will confirm shortly.', 'success')
    return redirect(url_for('patient_dashboard'))


@app.route('/patient/upload', methods=['POST'])
@login_required
def upload_record():
    file = request.files.get('record_file')
    if file and file.filename:
        original = secure_filename(file.filename)
        ext = original.rsplit('.', 1)[-1] if '.' in original else 'bin'
        filename = f"record_{current_user.id}_{int(datetime.utcnow().timestamp())}.{ext}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        rec = MedicalRecord(patient_id=current_user.id, filename=filename, original_name=original, file_type=ext)
        db.session.add(rec)
        db.session.commit()
        flash('Medical record uploaded successfully.', 'success')
    else:
        flash('Please select a file to upload.', 'error')
    return redirect(url_for('patient_dashboard'))


@app.route('/patient/message', methods=['POST'])
@login_required
def send_message():
    receiver_id = request.form.get('receiver_id')
    hospital_id = request.form.get('hospital_id')
    content = request.form.get('content', '').strip()
    if content:
        msg = Message(sender_id=current_user.id, receiver_id=receiver_id, hospital_id=hospital_id, content=content)
        db.session.add(msg)
        db.session.commit()
        flash('Message sent!', 'success')
    return redirect(url_for('patient_dashboard'))


# ─── Hospital Dashboard ─────────────────────────────────────────
@app.route('/hospital/dashboard')
@login_required
def hospital_dashboard():
    if current_user.role != 'hospital':
        return redirect(url_for('dashboard'))
    hospital = Hospital.query.filter_by(user_id=current_user.id).first()
    if not hospital:
        flash('Please complete your hospital profile first.', 'info')
        return render_template('hospital_setup.html')
    appointments = Appointment.query.filter_by(hospital_id=hospital.id).order_by(Appointment.created_at.desc()).all()
    messages = Message.query.filter_by(hospital_id=hospital.id).order_by(Message.created_at.desc()).limit(20).all()
    return render_template('hospital_dashboard.html', hospital=hospital, appointments=appointments, messages=messages)


@app.route('/hospital/setup', methods=['POST'])
@login_required
def hospital_setup():
    if current_user.role != 'hospital':
        return redirect(url_for('dashboard'))
    h = Hospital(
        user_id=current_user.id,
        name=request.form.get('name'),
        description=request.form.get('description', ''),
        country=request.form.get('country'),
        city=request.form.get('city'),
        address=request.form.get('address', ''),
        phone=request.form.get('phone', ''),
        email=request.form.get('email', ''),
        website=request.form.get('website', ''),
        specialties=json.dumps(request.form.getlist('specialties')),
        is_approved=False,
    )
    db.session.add(h)
    db.session.commit()
    flash('Hospital profile created! Awaiting admin approval.', 'success')
    return redirect(url_for('hospital_dashboard'))


@app.route('/hospital/appointment/<int:appt_id>/<action>')
@login_required
def manage_appointment(appt_id, action):
    appt = db.session.get(Appointment, appt_id) or abort(404)
    hospital = Hospital.query.filter_by(user_id=current_user.id).first()
    if not hospital or appt.hospital_id != hospital.id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('hospital_dashboard'))
    if action in ('confirmed', 'rejected', 'completed'):
        appt.status = action
        db.session.commit()
        flash(f'Appointment {action}.', 'success')
    return redirect(url_for('hospital_dashboard'))


@app.route('/hospital/package/add', methods=['POST'])
@login_required
def add_package():
    hospital = Hospital.query.filter_by(user_id=current_user.id).first()
    if not hospital:
        return redirect(url_for('hospital_dashboard'))
    pkg = Package(
        hospital_id=hospital.id,
        name=request.form.get('name'),
        description=request.form.get('description', ''),
        treatment_name=request.form.get('treatment_name', ''),
        includes_hotel='hotel' in request.form,
        includes_airport_pickup='airport' in request.form,
        includes_translator='translator' in request.form,
        includes_post_care='postcare' in request.form,
        hotel_details=request.form.get('hotel_details', ''),
        price=float(request.form.get('price', 0)),
        duration_days=int(request.form.get('duration_days', 7)),
    )
    db.session.add(pkg)
    db.session.commit()
    flash('Package added!', 'success')
    return redirect(url_for('hospital_dashboard'))


@app.route('/hospital/doctor/add', methods=['POST'])
@login_required
def add_doctor():
    hospital = Hospital.query.filter_by(user_id=current_user.id).first()
    if not hospital:
        return redirect(url_for('hospital_dashboard'))
    doc = Doctor(
        hospital_id=hospital.id,
        name=request.form.get('name'),
        specialty=request.form.get('specialty'),
        qualifications=request.form.get('qualifications', ''),
        experience_years=int(request.form.get('experience_years', 0)),
        bio=request.form.get('bio', ''),
        languages=json.dumps(request.form.get('languages', '').split(',')),
        consultation_fee=float(request.form.get('consultation_fee', 0)),
    )
    db.session.add(doc)
    db.session.commit()
    flash('Doctor profile added!', 'success')
    return redirect(url_for('hospital_dashboard'))


# ─── Admin Dashboard ─────────────────────────────────────────────
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    users = User.query.all()
    hospitals = Hospital.query.all()
    pending_hospitals = Hospital.query.filter_by(is_approved=False).all()
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(20).all()
    stats = {
        'total_users': User.query.count(),
        'total_hospitals': Hospital.query.count(),
        'total_doctors': Doctor.query.count(),
        'total_appointments': Appointment.query.count(),
        'pending_hospitals': len(pending_hospitals),
        'patients': User.query.filter_by(role='patient').count(),
    }
    return render_template('admin_dashboard.html', users=users, hospitals=hospitals, pending_hospitals=pending_hospitals, appointments=appointments, stats=stats)


@app.route('/admin/approve/<int:hospital_id>')
@login_required
def approve_hospital(hospital_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    h = db.session.get(Hospital, hospital_id) or abort(404)
    h.is_approved = True
    db.session.commit()
    flash(f'{h.name} has been approved!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete-user/<int:user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    user = db.session.get(User, user_id) or abort(404)
    if user.role == 'admin':
        flash('Cannot delete admin.', 'error')
        return redirect(url_for('admin_dashboard'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'success')
    return redirect(url_for('admin_dashboard'))


# ═════════════════════════════════════════════════════════════════
#  AI MATCHING API
# ═════════════════════════════════════════════════════════════════

@app.route('/finder')
def finder():
    return render_template('finder.html')


@app.route('/api/match', methods=['POST'])
def api_match():
    data = request.get_json(force=True)
    all_doctors = Doctor.query.filter_by(is_active=True).all()
    docs_dicts = []
    for d in all_doctors:
        h = db.session.get(Hospital, d.hospital_id)
        docs_dicts.append({
            'id': d.id,
            'name': d.name,
            'specialty': d.specialty,
            'country': h.country if h else '',
            'city': h.city if h else '',
            'hospital_name': h.name if h else '',
            'experience_years': d.experience_years,
            'consultation_fee': d.consultation_fee,
            'rating': d.rating,
            'review_count': d.review_count,
            'bio': d.bio or '',
            'qualifications': d.qualifications or '',
            'languages': d.languages or '[]',
            'image': d.image or '',
        })
    patient_info = {
        'specialty': data.get('specialty', ''),
        'budget': data.get('budget', 0),
        'country': data.get('country', ''),
        'min_experience': data.get('min_experience', 0),
    }
    ranked = calculate_match_scores(docs_dicts, patient_info)
    return jsonify(ranked[:5])


@app.route('/results')
def results():
    return render_template('results.html')


@app.route('/api/doctors')
def api_doctors():
    doctors = Doctor.query.filter_by(is_active=True).all()
    out = []
    for d in doctors:
        h = db.session.get(Hospital, d.hospital_id)
        out.append({
            'id': d.id, 'name': d.name, 'specialty': d.specialty,
            'hospital': h.name if h else '', 'country': h.country if h else '',
            'experience_years': d.experience_years, 'rating': d.rating,
            'consultation_fee': d.consultation_fee,
        })
    return jsonify(out)


# ─── Language Switch ─────────────────────────────────────────────
@app.route('/set-language/<lang>')
def set_language(lang):
    session['language'] = lang
    if current_user.is_authenticated:
        current_user.language = lang
        db.session.commit()
    return redirect(request.referrer or url_for('home'))


# ─── Review ──────────────────────────────────────────────────────
@app.route('/review/<int:hospital_id>', methods=['POST'])
@login_required
def add_review(hospital_id):
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '')
    review = Review(patient_id=current_user.id, hospital_id=hospital_id, rating=rating, comment=comment)
    db.session.add(review)
    # Update hospital rating
    h = db.session.get(Hospital, hospital_id)
    db.session.flush()  # ensure the new review is persisted before re-querying
    reviews = Review.query.filter_by(hospital_id=hospital_id).all()
    h.review_count = len(reviews)
    h.rating = round(sum(r.rating for r in reviews) / len(reviews), 1)
    db.session.commit()
    flash('Thank you for your review!', 'success')
    return redirect(url_for('hospital_detail', hospital_id=hospital_id))


# ═════════════════════════════════════════════════════════════════
#  BOOTSTRAP
# ═════════════════════════════════════════════════════════════════

with app.app_context():
    db.create_all()
    seed_database()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)