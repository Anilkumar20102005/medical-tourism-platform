"""
HealinBelieve — Database Seeder
Populates the database with sample hospitals, doctors, treatments, and packages.
"""

import json
from models import db, User, Hospital, Doctor, Treatment, Package


def seed_database():
    """Seed with sample data if DB is empty."""
    if User.query.first():
        return  # already seeded

    # ── Admin ────────────────────────────────────────────────────
    admin = User(name='Admin', email='admin@healinbelieve.com', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)

    # ── Hospitals & their users ──────────────────────────────────
    hospitals_data = [
        {
            "user": {"name": "Apollo Hospitals", "email": "info@apollo.com", "country": "India"},
            "hospital": {
                "name": "Apollo Hospitals International",
                "description": "One of Asia's largest healthcare groups with 72 hospitals and over 5,000 beds. Internationally accredited with JCI certification, offering world-class cardiac, orthopedic, and organ transplant services.",
                "country": "India", "city": "Chennai",
                "address": "21 Greams Lane, Chennai 600006",
                "phone": "+91-44-2829-0200", "website": "https://www.apollohospitals.com",
                "image": "https://api.dicebear.com/7.x/identicon/svg?seed=apollo&backgroundColor=0369a1",
                "rating": 4.8, "review_count": 1240,
                "specialties": json.dumps(["Cardiology", "Orthopedics", "Oncology", "Neurology", "Organ Transplant"]),
                "accreditations": json.dumps(["JCI Accredited", "NABH Certified", "ISO 9001:2015"]),
                "is_approved": True,
            },
            "doctors": [
                {"name": "Dr. Prathap Reddy", "specialty": "Cardiology", "qualifications": "MBBS, MD, DM Cardiology (AIIMS)", "experience_years": 28, "bio": "Founder-chairman of Apollo Hospitals and pioneering interventional cardiologist with over 10,000 procedures.", "consultation_fee": 100, "languages": json.dumps(["English", "Hindi", "Telugu"]), "rating": 4.9, "review_count": 420, "image": "https://api.dicebear.com/7.x/initials/svg?seed=PR&backgroundColor=0369a1"},
                {"name": "Dr. Anita Sharma", "specialty": "Orthopedics", "qualifications": "MBBS, MS Ortho, Fellow Joint Replacement (UK)", "experience_years": 18, "bio": "Specialist in robotic knee replacement surgery with 3,000+ successful procedures.", "consultation_fee": 80, "languages": json.dumps(["English", "Hindi"]), "rating": 4.7, "review_count": 285, "image": "https://api.dicebear.com/7.x/initials/svg?seed=AS&backgroundColor=7c3aed"},
            ],
            "treatments": [
                {"name": "Coronary Bypass Surgery (CABG)", "category": "Cardiac Surgery", "description": "Open-heart bypass grafting with state-of-the-art hybrid catheterization labs.", "min_cost": 5000, "max_cost": 8000, "duration_days": 10, "success_rate": 98.5},
                {"name": "Total Knee Replacement", "category": "Orthopedics", "description": "Robotic-assisted total knee arthroplasty using the latest implant technology.", "min_cost": 4000, "max_cost": 6500, "duration_days": 7, "success_rate": 97.0},
                {"name": "Liver Transplant", "category": "Organ Transplant", "description": "Living-donor and cadaveric liver transplantation with comprehensive post-operative care.", "min_cost": 25000, "max_cost": 40000, "duration_days": 21, "success_rate": 92.0},
            ],
            "packages": [
                {"name": "Heart Care Premium Package", "description": "Complete cardiac care including surgery, 5-star hotel recovery, airport transfers, and 24/7 nursing support.", "treatment_name": "Coronary Bypass Surgery", "includes_hotel": True, "includes_airport_pickup": True, "includes_translator": True, "includes_post_care": True, "hotel_details": "Taj Coromandel, 10 nights", "price": 9500, "duration_days": 14, "image": "https://api.dicebear.com/7.x/shapes/svg?seed=heartpkg&backgroundColor=0ea5e9"},
                {"name": "Knee Replacement Value Pack", "description": "Bilateral knee replacement with physiotherapy, hotel stay, and sightseeing tour.", "treatment_name": "Total Knee Replacement", "includes_hotel": True, "includes_airport_pickup": True, "includes_translator": False, "includes_post_care": True, "hotel_details": "ITC Grand Chola, 7 nights", "price": 7200, "duration_days": 10, "image": "https://api.dicebear.com/7.x/shapes/svg?seed=kneepkg&backgroundColor=059669"},
            ],
        },
        {
            "user": {"name": "Charité Berlin", "email": "info@charite.de", "country": "Germany"},
            "hospital": {
                "name": "Charité – Universitätsmedizin Berlin",
                "description": "Europe's largest university hospital with 300 years of medical excellence. Home to Nobel Prize laureates and globally recognised for research-driven cancer, neurology, and cardiology programmes.",
                "country": "Germany", "city": "Berlin",
                "address": "Charitéplatz 1, 10117 Berlin",
                "phone": "+49-30-450-50", "website": "https://www.charite.de",
                "image": "https://api.dicebear.com/7.x/identicon/svg?seed=charite&backgroundColor=7c3aed",
                "rating": 4.9, "review_count": 890,
                "specialties": json.dumps(["Oncology", "Neurology", "Cardiology", "Immunology", "Transplant Surgery"]),
                "accreditations": json.dumps(["JCI Accredited", "German Hospital Federation", "EU Research Excellence"]),
                "is_approved": True,
            },
            "doctors": [
                {"name": "Dr. Elena Fischer", "specialty": "Cardiology", "qualifications": "MD, FESC, Fellowship Interventional Cardiology", "experience_years": 22, "bio": "Leading interventional cardiologist specialising in complex coronary interventions and structural heart disease. Published 85+ peer-reviewed papers.", "consultation_fee": 250, "languages": json.dumps(["English", "German", "French"]), "rating": 4.8, "review_count": 310, "image": "https://api.dicebear.com/7.x/initials/svg?seed=EF&backgroundColor=7c3aed"},
                {"name": "Dr. Hans Mueller", "specialty": "Oncology", "qualifications": "MD, PhD, Board Certified Oncologist", "experience_years": 25, "bio": "Pioneer in immunotherapy and precision oncology research. Leads Charité's Comprehensive Cancer Center.", "consultation_fee": 300, "languages": json.dumps(["English", "German"]), "rating": 4.9, "review_count": 198, "image": "https://api.dicebear.com/7.x/initials/svg?seed=HM&backgroundColor=dc2626"},
            ],
            "treatments": [
                {"name": "Immunotherapy Cancer Treatment", "category": "Oncology", "description": "Personalised checkpoint inhibitor and CAR-T cell therapy for advanced cancers.", "min_cost": 15000, "max_cost": 45000, "duration_days": 30, "success_rate": 78.0},
                {"name": "Deep Brain Stimulation", "category": "Neurology", "description": "Minimally invasive DBS for Parkinson's disease and essential tremor.", "min_cost": 20000, "max_cost": 35000, "duration_days": 14, "success_rate": 88.0},
            ],
            "packages": [
                {"name": "Cancer Treatment Excellence", "description": "Full immunotherapy course with Berlin luxury hotel, private transfers, interpreter, and follow-up teleconsultations.", "treatment_name": "Immunotherapy Cancer Treatment", "includes_hotel": True, "includes_airport_pickup": True, "includes_translator": True, "includes_post_care": True, "hotel_details": "Hotel Adlon Kempinski, 30 nights", "price": 52000, "duration_days": 35, "image": "https://api.dicebear.com/7.x/shapes/svg?seed=cancerpkg&backgroundColor=7c3aed"},
            ],
        },
        {
            "user": {"name": "Bumrungrad International", "email": "info@bumrungrad.com", "country": "Thailand"},
            "hospital": {
                "name": "Bumrungrad International Hospital",
                "description": "Thailand's premier medical tourism destination serving over 1.1 million patients annually from 190+ countries. Multi-award-winning for patient safety and medical excellence.",
                "country": "Thailand", "city": "Bangkok",
                "address": "33 Sukhumvit 3, Bangkok 10110",
                "phone": "+66-2-066-8888", "website": "https://www.bumrungrad.com",
                "image": "https://api.dicebear.com/7.x/identicon/svg?seed=bumrungrad&backgroundColor=059669",
                "rating": 4.7, "review_count": 2100,
                "specialties": json.dumps(["Cosmetic Surgery", "Dental Care", "Fertility", "Dermatology", "Wellness"]),
                "accreditations": json.dumps(["JCI Accredited", "GHA Certified", "Thailand Centre of Excellence"]),
                "is_approved": True,
            },
            "doctors": [
                {"name": "Dr. Somchai Prasert", "specialty": "Dermatology", "qualifications": "MD, Thai Board of Dermatology, Fellow Cosmetic Derm (Seoul)", "experience_years": 15, "bio": "Expert in cosmetic dermatology and advanced laser treatments combining Thai holistic philosophy with cutting-edge aesthetics.", "consultation_fee": 90, "languages": json.dumps(["English", "Thai", "Mandarin"]), "rating": 4.7, "review_count": 195, "image": "https://api.dicebear.com/7.x/initials/svg?seed=SP&backgroundColor=059669"},
                {"name": "Dr. Naree Suwanpakdee", "specialty": "Cosmetic Surgery", "qualifications": "MD, FACS, Board Certified Plastic Surgeon", "experience_years": 20, "bio": "Renowned cosmetic surgeon specialising in rhinoplasty, facelifts, and body contouring with natural-looking results.", "consultation_fee": 150, "languages": json.dumps(["English", "Thai"]), "rating": 4.8, "review_count": 340, "image": "https://api.dicebear.com/7.x/initials/svg?seed=NS&backgroundColor=d97706"},
            ],
            "treatments": [
                {"name": "Rhinoplasty", "category": "Cosmetic Surgery", "description": "Nose reshaping surgery with 3D imaging planning and minimal-scar techniques.", "min_cost": 2500, "max_cost": 5000, "duration_days": 5, "success_rate": 96.0},
                {"name": "Dental Veneers (Full Set)", "category": "Dental Care", "description": "Premium porcelain veneers for a complete smile makeover.", "min_cost": 3000, "max_cost": 6000, "duration_days": 5, "success_rate": 99.0},
                {"name": "IVF Fertility Treatment", "category": "Fertility", "description": "Full IVF cycle including consultation, egg retrieval, embryo transfer, and monitoring.", "min_cost": 4000, "max_cost": 7000, "duration_days": 21, "success_rate": 55.0},
            ],
            "packages": [
                {"name": "Bangkok Beauty Package", "description": "Rhinoplasty + dental veneers combo with luxury spa hotel, airport limousine, and Bangkok sightseeing.", "treatment_name": "Rhinoplasty + Dental Veneers", "includes_hotel": True, "includes_airport_pickup": True, "includes_translator": True, "includes_post_care": True, "hotel_details": "The Siam Hotel, 7 nights", "price": 8500, "duration_days": 10, "image": "https://api.dicebear.com/7.x/shapes/svg?seed=beautypkg&backgroundColor=d97706"},
                {"name": "Fertility Hope Package", "description": "Complete IVF cycle with beachside recovery hotel, private nurse, and Thai wellness spa sessions.", "treatment_name": "IVF Fertility Treatment", "includes_hotel": True, "includes_airport_pickup": True, "includes_translator": True, "includes_post_care": True, "hotel_details": "Mandarin Oriental, 21 nights", "price": 9800, "duration_days": 25, "image": "https://api.dicebear.com/7.x/shapes/svg?seed=ivfpkg&backgroundColor=0891b2"},
            ],
        },
        {
            "user": {"name": "Samsung Medical Center", "email": "info@samsung-med.com", "country": "South Korea"},
            "hospital": {
                "name": "Samsung Medical Center",
                "description": "South Korea's top-ranked hospital with cutting-edge robotic surgery, precision medicine, and advanced cancer treatment programmes attracting patients from 60+ countries.",
                "country": "South Korea", "city": "Seoul",
                "address": "81 Irwon-ro, Gangnam-gu, Seoul",
                "phone": "+82-2-3410-0200", "website": "https://www.samsunghospital.com",
                "image": "https://api.dicebear.com/7.x/identicon/svg?seed=samsung&backgroundColor=dc2626",
                "rating": 4.9, "review_count": 760,
                "specialties": json.dumps(["Neurology", "Oncology", "Robotic Surgery", "Ophthalmology", "Cardiology"]),
                "accreditations": json.dumps(["JCI Accredited", "KOHCA Certified", "Global Healthcare Excellence"]),
                "is_approved": True,
            },
            "doctors": [
                {"name": "Dr. Yuki Tanaka", "specialty": "Neurology", "qualifications": "MD, Korean Board of Neurology, Fellow Epilepsy (Mayo Clinic)", "experience_years": 20, "bio": "Globally recognised neurology expert specialising in epilepsy and neuro-degenerative disorders. Directs the Brain Research Institute.", "consultation_fee": 200, "languages": json.dumps(["English", "Korean", "Japanese"]), "rating": 4.9, "review_count": 260, "image": "https://api.dicebear.com/7.x/initials/svg?seed=YT&backgroundColor=dc2626"},
                {"name": "Dr. Min-Jun Park", "specialty": "Robotic Surgery", "qualifications": "MD, PhD, FACS, Da Vinci Certified Surgeon", "experience_years": 16, "bio": "Pioneer in robotic-assisted minimally invasive surgery for prostate, kidney, and colorectal cancers.", "consultation_fee": 220, "languages": json.dumps(["English", "Korean"]), "rating": 4.8, "review_count": 175, "image": "https://api.dicebear.com/7.x/initials/svg?seed=MP&backgroundColor=0891b2"},
            ],
            "treatments": [
                {"name": "Robotic Prostate Surgery", "category": "Robotic Surgery", "description": "Da Vinci robotic-assisted radical prostatectomy with faster recovery and fewer side effects.", "min_cost": 12000, "max_cost": 18000, "duration_days": 7, "success_rate": 96.0},
                {"name": "LASIK Eye Surgery", "category": "Ophthalmology", "description": "Bladeless femtosecond LASIK with wavefront-guided technology for perfect vision correction.", "min_cost": 1500, "max_cost": 3000, "duration_days": 2, "success_rate": 99.5},
            ],
            "packages": [
                {"name": "Seoul Precision Surgery", "description": "Robotic surgery with Gangnam luxury hotel, K-culture experience, private transfers, and telemedicine follow-up.", "treatment_name": "Robotic Prostate Surgery", "includes_hotel": True, "includes_airport_pickup": True, "includes_translator": True, "includes_post_care": True, "hotel_details": "Park Hyatt Seoul, 10 nights", "price": 22000, "duration_days": 12, "image": "https://api.dicebear.com/7.x/shapes/svg?seed=seoulpkg&backgroundColor=dc2626"},
            ],
        },
        {
            "user": {"name": "Acibadem Healthcare", "email": "info@acibadem.com", "country": "Turkey"},
            "hospital": {
                "name": "Acıbadem Healthcare Group",
                "description": "Turkey's leading private healthcare network with 23 hospitals, renowned for affordable high-quality oncology, transplant, and cosmetic surgery procedures attracting 750,000+ international patients.",
                "country": "Turkey", "city": "Istanbul",
                "address": "Altunizade Mah, Fahrettin Kerim Gokay Cad, Istanbul",
                "phone": "+90-212-304-4444", "website": "https://www.acibadem.com",
                "image": "https://api.dicebear.com/7.x/identicon/svg?seed=acibadem&backgroundColor=d97706",
                "rating": 4.6, "review_count": 1580,
                "specialties": json.dumps(["Oncology", "Hair Transplant", "Dental Care", "Cardiac Surgery", "Fertility"]),
                "accreditations": json.dumps(["JCI Accredited", "ISO 9001", "Turkish Health Tourism Authorization"]),
                "is_approved": True,
            },
            "doctors": [
                {"name": "Dr. Ayşe Demir", "specialty": "Oncology", "qualifications": "MD, ESMO Certified, Fellow Immuno-Oncology (MD Anderson)", "experience_years": 17, "bio": "Trailblazer in immuno-oncology and precision medicine. Combines genomic profiling with personalised therapy.", "consultation_fee": 150, "languages": json.dumps(["English", "Turkish", "Arabic"]), "rating": 4.8, "review_count": 230, "image": "https://api.dicebear.com/7.x/initials/svg?seed=AD&backgroundColor=d97706"},
                {"name": "Dr. Mehmet Kaya", "specialty": "Hair Transplant", "qualifications": "MD, ISHRS Member, DHI Certified", "experience_years": 12, "bio": "One of Turkey's most sought-after hair restoration specialists with 8,000+ FUE procedures and natural hairline artistry.", "consultation_fee": 80, "languages": json.dumps(["English", "Turkish", "Arabic", "Russian"]), "rating": 4.7, "review_count": 520, "image": "https://api.dicebear.com/7.x/initials/svg?seed=MK&backgroundColor=059669"},
            ],
            "treatments": [
                {"name": "FUE Hair Transplant (3,000 grafts)", "category": "Hair Transplant", "description": "Follicular Unit Extraction with sapphire blade micro-channels for denser, natural-looking results.", "min_cost": 1500, "max_cost": 3500, "duration_days": 3, "success_rate": 95.0},
                {"name": "All-on-4 Dental Implants", "category": "Dental Care", "description": "Full-arch dental rehabilitation with 4 titanium implants and same-day temporary teeth.", "min_cost": 4000, "max_cost": 7000, "duration_days": 5, "success_rate": 97.0},
            ],
            "packages": [
                {"name": "Istanbul Hair Revival", "description": "FUE hair transplant with Bosphorus-view hotel, airport VIP transfer, PRP sessions, and Istanbul city tour.", "treatment_name": "FUE Hair Transplant", "includes_hotel": True, "includes_airport_pickup": True, "includes_translator": True, "includes_post_care": True, "hotel_details": "Raffles Istanbul, 5 nights", "price": 4500, "duration_days": 7, "image": "https://api.dicebear.com/7.x/shapes/svg?seed=hairpkg&backgroundColor=d97706"},
                {"name": "Smile Makeover Istanbul", "description": "Complete dental implant treatment with luxury hotel stay, personal guide, and Bosphorus cruise.", "treatment_name": "All-on-4 Dental Implants", "includes_hotel": True, "includes_airport_pickup": True, "includes_translator": True, "includes_post_care": True, "hotel_details": "Four Seasons Sultanahmet, 7 nights", "price": 8500, "duration_days": 8, "image": "https://api.dicebear.com/7.x/shapes/svg?seed=dentalpkg&backgroundColor=0369a1"},
            ],
        },
    ]

    for hdata in hospitals_data:
        # Create hospital user
        hu = User(name=hdata["user"]["name"], email=hdata["user"]["email"], role='hospital', country=hdata["user"]["country"])
        hu.set_password('hospital123')
        db.session.add(hu)
        db.session.flush()

        # Create hospital
        h = Hospital(user_id=hu.id, **hdata["hospital"])
        db.session.add(h)
        db.session.flush()

        # Create doctors
        for dd in hdata["doctors"]:
            doc = Doctor(hospital_id=h.id, **dd)
            db.session.add(doc)

        # Create treatments
        for td in hdata["treatments"]:
            tr = Treatment(hospital_id=h.id, **td)
            db.session.add(tr)

        # Create packages
        for pd in hdata["packages"]:
            pkg = Package(hospital_id=h.id, **pd)
            db.session.add(pkg)

    # ── Sample patient ───────────────────────────────────────────
    patient = User(name='John Smith', email='patient@example.com', role='patient', country='USA')
    patient.set_password('patient123')
    db.session.add(patient)

    db.session.commit()
    print("[OK] Database seeded successfully!")
