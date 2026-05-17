import json
from datetime import datetime, timedelta
from random import choice, randint, uniform

# Sample data generation functions
def generate_id():
    return ''.join(choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for _ in range(10))

def generate_working_hours():
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    return [
        {
            "day_of_week": day,
            "is_open": choice([True, False]),
            "open_time": f"{randint(8, 12)}:00",
            "close_time": f"{randint(13, 18)}:00"
        } for day in days
    ]

def generate_doctor_working_hours():
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    return [
        {
            "day_of_week": day,
            "is_available": choice([True, False]),
            "start_time": f"{randint(8, 12)}:00",
            "end_time": f"{randint(13, 18)}:00",
            "break_start_time": f"{randint(12, 16)}:00",
            "break_end_time": f"{randint(13, 17)}:00"
        } for day in days
    ]

def generate_appointment_date():
    return (datetime.now() + timedelta(days=randint(1, 30))).strftime("%Y-%M-%d")

def generate_appointment_time():
    return f"{randint(8, 17)}:{choice(['00', '30'])}"

def generate_booking_code():
    return f"APT-{generate_id()}"

# Sample data
hospitals = [
    {
        "id": generate_id(),
        "name": "City General Hospital",
        "slug": "city-general-hospital",
        "description": "A general hospital providing a wide range of medical services.",
        "address": "123 Health St, Cityville",
        "phone": "+1234567890",
        "email": "info@citygeneral.com",
        "image_url": "https://example.com/city-general.jpg",
        "emergency_available": True,
        "working_hours": generate_working_hours(),
        "departments": [],
        "doctors": []
    },
    {
        "id": generate_id(),
        "name": "Sunrise Medical Center",
        "slug": "sunrise-medical-center",
        "description": "A modern medical center with advanced facilities.",
        "address": "456 Wellness Ave, Sunnyside",
        "phone": "+0987654321",
        "email": "contact@sunrisemedical.com",
        "image_url": "https://example.com/sunrise-medical.jpg",
        "emergency_available": False,
        "working_hours": generate_working_hours(),
        "departments": [],
        "doctors": []
    },
    {
        "id": generate_id(),
        "name": "Greenview Clinic",
        "slug": "greenview-clinic",
        "description": "A community clinic offering primary care services.",
        "address": "789 Green Rd, Greentown",
        "phone": "+1122334455",
        "email": "info@greenviewclinic.com",
        "image_url": "https://example.com/greenview-clinic.jpg",
        "emergency_available": True,
        "working_hours": generate_working_hours(),
        "departments": [],
        "doctors": []
    }
]

departments = [
    {
        "id": generate_id(),
        "name": "Cardiology",
        "slug": "cardiology",
        "description": "Specialized in heart diseases and treatments.",
        "icon_url": "https://example.com/cardiology.png",
        "hospital_id": hospitals[0]["id"]
    },
    {
        "id": generate_id(),
        "name": "Pediatrics",
        "slug": "pediatrics",
        "description": "Caring for children's health needs.",
        "icon_url": "https://example.com/pediatrics.png",
        "hospital_id": hospitals[0]["id"]
    },
    {
        "id": generate_id(),
        "name": "Neurology",
        "slug": "neurology",
        "description": "Expertise in brain and nervous system disorders.",
        "icon_url": "https://example.com/neurology.png",
        "hospital_id": hospitals[1]["id"]
    },
    {
        "id": generate_id(),
        "name": "Orthopedics",
        "slug": "orthopedics",
        "description": "Treating musculoskeletal conditions.",
        "icon_url": "https://example.com/orthopedics.png",
        "hospital_id": hospitals[1]["id"]
    },
    {
        "id": generate_id(),
        "name": "Dermatology",
        "slug": "dermatology",
        "description": "Specializing in skin health.",
        "icon_url": "https://example.com/dermatology.png",
        "hospital_id": hospitals[2]["id"]
    },
    {
        "id": generate_id(),
        "name": "Gynecology",
        "slug": "gynecology",
        "description": "Women's health services.",
        "icon_url": "https://example.com/gynecology.png",
        "hospital_id": hospitals[2]["id"]
    },
    {
        "id": generate_id(),
        "name": "Oncology",
        "slug": "oncology",
        "description": "Cancer treatment and support.",
        "icon_url": "https://example.com/oncology.png",
        "hospital_id": hospitals[0]["id"]
    },
    {
        "id": generate_id(),
        "name": "Psychiatry",
        "slug": "psychiatry",
        "description": "Mental health services.",
        "icon_url": "https://example.com/psychiatry.png",
        "hospital_id": hospitals[1]["id"]
    },
    {
        "id": generate_id(),
        "name": "Endocrinology",
        "slug": "endocrinology",
        "description": "Diabetes and hormonal disorders.",
        "icon_url": "https://example.com/endocrinology.png",
        "hospital_id": hospitals[2]["id"]
    },
    {
        "id": generate_id(),
        "name": "Urology",
        "slug": "urology",
        "description": "Conditions affecting the urinary system.",
        "icon_url": "https://example.com/urology.png",
        "hospital_id": hospitals[0]["id"]
    }
]

doctors = [
    {
        "id": generate_id(),
        "full_name": "Dr. John Doe",
        "slug": "dr-john-doe",
        "photo_url": "https://example.com/johndoe.jpg",
        "specialization": "Cardiology",
        "department_id": departments[0]["id"],
        "hospital_id": hospitals[0]["id"],
        "experience_years": randint(5, 20),
        "qualifications": "MBBS, MD",
        "bio": "Experienced cardiologist with a focus on heart disease prevention.",
        "consultation_fee": round(uniform(50.0, 200.0), 2),
        "languages": ["English", "Spanish"],
        "rating": round(uniform(3.5, 5.0), 1),
        "gender": "Male",
        "working_hours": generate_doctor_working_hours(),
        "appointment_duration_minutes": 30
    },
    {
        "id": generate_id(),
        "full_name": "Dr. Jane Smith",
        "slug": "dr-jane-smith",
        "photo_url": "https://example.com/janesmith.jpg",
        "specialization": "Pediatrics",
        "department_id": departments[1]["id"],
        "hospital_id": hospitals[0]["id"],
        "experience_years": randint(5, 20),
        "qualifications": "MBBS, DCH",
        "bio": "Child specialist with expertise in pediatric care.",
        "consultation_fee": round(uniform(50.0, 200.0), 2),
        "languages": ["English", "French"],
        "rating": round(uniform(3.5, 5.0), 1),
        "gender": "Female",
        "working_hours": generate_doctor_working_hours(),
        "appointment_duration_minutes": 30
    },
    {
        "id": generate_id(),
        "full_name": "Dr. Alex Johnson",
        "slug": "dr-alex-johnson",
        "photo_url": "https://example.com/alexjohnson.jpg",
        "specialization": "Neurology",
        "department_id": departments[2]["id"],
        "hospital_id": hospitals[1]["id"],
        "experience_years": randint(5, 20),
        "qualifications": "MBBS, DM",
        "bio": "Neurologist with a focus on neurological disorders.",
        "consultation_fee": round(uniform(50.0, 200.0), 2),
        "languages": ["English"],
        "rating": round(uniform(3.5, 5.0), 1),
        "gender": "Male",
        "working_hours": generate_doctor_working_hours(),
        "appointment_duration_minutes": 30
    },
    {
        "id": generate_id(),
        "full_name": "Dr. Emily Davis",
        "slug": "dr-emily-davis",
        "photo_url": "https://example.com/emilydavis.jpg",
        "specialization": "Orthopedics",
        "department_id": departments[3]["id"],
        "hospital_id": hospitals[1]["id"],
        "experience_years": randint(5, 20),
        "qualifications": "MBBS, MS",
        "bio": "Orthopedic surgeon with expertise in joint replacements.",
        "consultation_fee": round(uniform(50.0, 200.0), 2),
        "languages": ["English", "German"],
        "rating": round(uniform(3.5, 5.0), 1),
        "gender": "Female",
        "working_hours": generate_doctor_working_hours(),
        "appointment_duration_minutes": 30
    },
    {
        "id": generate_id(),
        "full_name": "Dr. Michael Brown",
        "slug": "dr-michael-brown",
        "photo_url": "https://example.com/michaelbrown.jpg",
        "specialization": "Dermatology",
        "department_id": departments[4]["id"],
        "hospital_id": hospitals[2]["id"],
        "experience_years": randint(5, 20),
        "qualifications": "MBBS, MD",
        "bio": "Dermatologist with a focus on skin cancer prevention.",
        "consultation_fee": round(uniform(50.0, 200.0), 2),
        "languages": ["English"],
        "rating": round(uniform(3.5, 5.0), 1),
        "gender": "Male",
        "working_hours": generate_doctor_working_hours(),
        "appointment_duration_minutes": 30
    },
    {
        "id": generate_id(),
        "full_name": "Dr. Sarah Lee",
        "slug": "dr-sarah-lee",
        "photo_url": "https://example.com/sarahlee.jpg",
        "specialization": "Gynecology",
        "department_id": departments[5]["id"],
        "hospital_id": hospitals[2]["id"],
        "experience_years": randint(5, 20),
        "qualifications": "MBBS, DGO",
        "bio": "Gynecologist with expertise in women's reproductive health.",
        "consultation_fee": round(uniform(50.0, 200.0), 2),
        "languages": ["English", "Chinese"],
        "rating": round(uniform(3.5, 5.0), 1),
        "gender": "Female",
        "working_hours": generate_doctor_working_hours(),
        "appointment_duration_minutes": 30
    },
    {
        "id": generate_id(),
        "full_name": "Dr. David Wilson",
        "slug": "dr-david-wilson",
        "photo_url": "https://example.com/davidwilson.jpg",
        "specialization": "Oncology",
        "department_id": departments[6]["id"],
        "hospital_id": hospitals[0]["id"],
        "experience_years": randint(5, 20),
        "qualifications": "MBBS, MD",
        "bio": "Oncologist with a focus on cancer treatment.",
        "consultation_fee": round(uniform(50.0, 200.0), 2),
        "languages": ["English"],
        "rating": round(uniform(3.5, 5.0), 1),
        "gender": "Male",
        "working_hours": generate_doctor_working_hours(),
        "appointment_duration_minutes": 30
    },
    {
        "id": generate_id(),
        "full_name": "Dr. Olivia Martinez",
        "slug": "dr-olivia-martinez",
        "photo_url": "https://example.com/oliviamartinez.jpg",
        "specialization": "Psychiatry",
        "department_id": departments[7]["id"],
        "hospital_id": hospitals[1]["id"],
        "experience_years": randint(5, 20),
        "qualifications": "MBBS, MD",
        "bio": "Psychiatrist with expertise in mental health disorders.",
        "consultation_fee": round(uniform(50.0, 200.0), 2),
        "languages": ["English", "Spanish"],
        "rating": round(uniform(3.5, 5.0), 1),
        "gender": "Female",
        "working_hours": generate_doctor_working_hours(),
        "appointment_duration_minutes": 30
    },
    {
        "id": generate_id(),
        "full_name": "Dr. William Taylor",
        "slug": "dr-william-taylor",
        "photo_url": "https://example.com/williamtaylor.jpg",
        "specialization": "Endocrinology",
        "department_id": departments[8]["id"],
        "hospital_id": hospitals[2]["id"],
        "experience_years": randint(5, 20),
        "qualifications": "MBBS, MD",
        "bio": "Endocrinologist with a focus on diabetes management.",
        "consultation_fee": round(uniform(50.0, 200.0), 2),
        "languages": ["English"],
        "rating": round(uniform(3.5, 5.0), 1),
        "gender": "Male",
        "working_hours": generate_doctor_working_hours(),
        "appointment_duration_minutes": 30
    },
    {
        "id": generate_id(),
        "full_name": "Dr. Sophia Anderson",
        "slug": "dr-sophia-anderson",
        "photo_url": "https://example.com/sophiaanderson.jpg",
        "specialization": "Urology",
        "department_id": departments[9]["id"],
        "hospital_id": hospitals[0]["id"],
        "experience_years": randint(5, 20),
        "qualifications": "MBBS, MS",
        "bio": "Urologist with expertise in urinary tract disorders.",
        "consultation_fee": round(uniform(50.0, 200.0), 2),
        "languages": ["English", "French"],
        "rating": round(uniform(3.5, 5.0), 1),
        "gender": "Female",
        "working_hours": generate_doctor_working_hours(),
        "appointment_duration_minutes": 30
    }
]

appointments = [
    {
        "id": generate_id(),
        "booking_code": generate_booking_code(),
        "hospital_id": hospitals[0]["id"],
        "department_id": departments[0]["id"],
        "doctor_id": doctors[0]["id"],
        "patient_name": "John Patient",
        "patient_phone": "+1234567890",
        "patient_email": "john@example.com",
        "patient_age": randint(18, 80),
        "patient_gender": choice(["Male", "Female"]),
        "reason_for_visit": "Heart check-up",
        "appointment_date": generate_appointment_date(),
        "appointment_time": generate_appointment_time(),
        "status": "pending",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": generate_id(),
        "booking_code": generate_booking_code(),
        "hospital_id": hospitals[1]["id"],
        "department_id": departments[2]["id"],
        "doctor_id": doctors[2]["id"],
        "patient_name": "Jane Patient",
        "patient_phone": "+0987654321",
        "patient_email": "jane@example.com",
        "patient_age": randint(18, 80),
        "patient_gender": choice(["Male", "Female"]),
        "reason_for_visit": "Headache",
        "appointment_date": generate_appointment_date(),
        "appointment_time": generate_appointment_time(),
        "status": "confirmed",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": generate_id(),
        "booking_code": generate_booking_code(),
        "hospital_id": hospitals[2]["id"],
        "department_id": departments[4]["id"],
        "doctor_id": doctors[4]["id"],
        "patient_name": "Mike Patient",
        "patient_phone": "+1122334455",
        "patient_email": "mike@example.com",
        "patient_age": randint(18, 80),
        "patient_gender": choice(["Male", "Female"]),
        "reason_for_visit": "Skin rash",
        "appointment_date": generate_appointment_date(),
        "appointment_time": generate_appointment_time(),
        "status": "cancelled",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": generate_id(),
        "booking_code": generate_booking_code(),
        "hospital_id": hospitals[0]["id"],
        "department_id": departments[6]["id"],
        "doctor_id": doctors[6]["id"],
        "patient_name": "Lily Patient",
        "patient_phone": "+5554443333",
        "patient_email": "lily@example.com",
        "patient_age": randint(18, 80),
        "patient_gender": choice(["Male", "Female"]),
        "reason_for_visit": "Breast cancer screening",
        "appointment_date": generate_appointment_date(),
        "appointment_time": generate_appointment_time(),
        "status": "completed",
        "created_at": datetime.now().isoformat()
    },
    {
        "id": generate_id(),
        "booking_code": generate_booking_code(),
        "hospital_id": hospitals[1]["id"],
        "department_id": departments[7]["id"],
        "doctor_id": doctors[7]["id"],
        "patient_name": "Tom Patient",
        "patient_phone": "+6667778888",
        "patient_email": "tom@example.com",
        "patient_age": randint(18, 80),
        "patient_gender": choice(["Male", "Female"]),
        "reason_for_visit": "Anxiety",
        "appointment_date": generate_appointment_date(),
        "appointment_time": generate_appointment_time(),
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
]

# Assign departments and doctors to hospitals
for hospital in hospitals:
    hospital["departments"] = [dept["id"] for dept in departments if dept["hospital_id"] == hospital["id"]]
    hospital["doctors"] = [doc["id"] for doc in doctors if doc["hospital_id"] == hospital["id"]]

# Save to db.json
db = {
    "hospitals": hospitals,
    "departments": departments,
    "doctors": doctors,
    "appointments": appointments
}

with open("db.json", "w") as f:
    json.dump(db, f, indent=2)