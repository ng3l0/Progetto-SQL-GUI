import sqlite3
from datetime import datetime, timedelta, time as dtime


conn = sqlite3.connect("Database_proj.db")
cursor = conn.cursor()

#cursor.execute("DROP TABLE IF EXISTS Questionnaire;")
#cursor.execute("DROP TABLE IF EXISTS AvailableSlots;")
#cursor.execute("DROP TABLE IF EXISTS Appointments;")
# ========== TABELLE ==========

# Patients
cursor.execute("""
CREATE TABLE IF NOT EXISTS Patients (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Surname TEXT NOT NULL,
    dateOfBirth DATE,
    height REAL CHECK(height > 0),
    weight REAL CHECK(weight > 0),
    Age INTEGER CHECK(Age > 0),
    Gender CHAR(1) CHECK(Gender IN ('M', 'F', 'O')),
    Nationality TEXT DEFAULT 'Italian',
    ClinicalHistory TEXT,
    PatientID TEXT NOT NULL UNIQUE,
    PatientPassword TEXT,
    PhoneNumber TEXT UNIQUE
);
""")

#questionario
cursor.execute("""
CREATE TABLE IF NOT EXISTS Questionnaire (
    QuestID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Date DATE,

    Q1 INTEGER,
    Q2 INTEGER,
    Nota2 TEXT,

    Q3 INTEGER,

    Q4 INTEGER,
    Q5 INTEGER,
    Q6 INTEGER,
    Q7 INTEGER,

    Q8 INTEGER,
    Q9 TEXT,

    Q10 INTEGER,
    Q11 TEXT,

    Q12 INTEGER,
    Q13 TEXT
);
""")
conn.commit()

# Doctors
cursor.execute("""
CREATE TABLE IF NOT EXISTS Doctors (
    Name TEXT NOT NULL,
    Surname TEXT NOT NULL,
    dateOfBirth DATE,
    doctorID TEXT PRIMARY KEY,
    hospital TEXT,
    DoctorPassword TEXT,
    PhoneNumber TEXT UNIQUE
);
""")

# Patients_OK
cursor.execute("""
CREATE TABLE IF NOT EXISTS Patients_OK (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Date DATE,
    Days_since_last_OSA INTEGER,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

# Patients_Follow_up
cursor.execute("""
CREATE TABLE IF NOT EXISTS Patients_Follow_up (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Date DATE,
    Days_since_last_OSA INTEGER,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

# Drugs
cursor.execute("""
CREATE TABLE IF NOT EXISTS Drugs (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Note TEXT,
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

# Therapy
cursor.execute("""
CREATE TABLE IF NOT EXISTS Therapy (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Note TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

#appuntamenti
cursor.execute("""
CREATE TABLE IF NOT EXISTS Appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    doctor_id TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'available',
    patient_id TEXT,
    patient_name TEXT,
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctorID),
    FOREIGN KEY (patient_id) REFERENCES Patients(PatientID)
);
""")

#notifiche paziente
cursor.execute("""
CREATE TABLE Notifications (
         NotificationID INTEGER PRIMARY KEY AUTOINCREMENT,
         PatientID TEXT,
         PatientName TEXT,
         Type TEXT,  -- 'REMINDER', 'DOCTOR_ALERT', etc.
         Message TEXT,
         Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
         IsRead BOOLEAN DEFAULT 0,
         FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
     );
""")
# ========== INSERIMENTI ==========

# Doctors
# cursor.execute("""
# INSERT INTO Doctors (Name, Surname, doctorID, DoctorPassword, dateOfBirth, hospital, PhoneNumber)
# VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("Mario", "Rossi", "DOC001", "password123", "1980-01-01", "Ospedale San Giovanni", "1234567890"))

#cursor.execute("""
# INSERT INTO Doctors (Name, Surname, doctorID, DoctorPassword, dateOfBirth, hospital, PhoneNumber)
# VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("Anna", "Vincentelli", "DOC002", "password345", "1970-01-01", "Ospedale Galeazzi", "1234567777"))

# Patients
# cursor.execute("""
# INSERT INTO Patients (Name, Surname, dateOfBirth, height, weight, Age, Gender, Nationality, ClinicalHistory, PatientID, PatientPassword, PhoneNumber)
# VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# """, ("Luca", "Bianchi", "2000-05-15", 1.75, 70, 33, "M", "Italiano", "Nessuna", "PAT001", "password123", "1234567890"))

#cursor.execute("""
# INSERT INTO Patients (Name, Surname, dateOfBirth, height, weight, Age, Gender, Nationality, ClinicalHistory, PatientID, PatientPassword, PhoneNumber)
# VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# """, ("Lucia", "Garofalo", "2004-06-15", 1.65, 60, 25, "F", "Italiano", "Nessuna", "PAT002", "345678", "1234567899"))

# Patients_OK
# cursor.execute("""
# INSERT INTO Patients_OK (PatientID, Date, Days_since_last_OSA)
# VALUES (?, ?, ?)
# """, ("PAT001", "2025-04-25", 9))

# Patients_Follow_up
cursor.execute("""
INSERT INTO Patients_Follow_up (PatientID, Date, Days_since_last_OSA)
VALUES (?, ?, ?)
""", ("PAT002", "2025-04-26", 2))

# Drugs
cursor.execute("""
INSERT INTO Drugs (PatientID, Note, StartDate, EndDate)
VALUES (?, ?, ?, ?)
""", ("PAT001", "Paracetamolo 500mg 2 volte al giorno", "2025-04-20", "2025-04-27"))

cursor.execute("""
INSERT INTO Drugs (PatientID, Note, StartDate, EndDate)
VALUES (?, ?, ?, ?)
""", ("PAT002", "Ibuprofene al bisogno", "2025-04-21", "2025-04-25"))

# Therapy
cursor.execute("""
INSERT INTO Therapy (PatientID, Note)
VALUES (?, ?)
""", ("PAT001", "Monitoraggio continuo con eventuale follow-up dopo 10 giorni"))

cursor.execute("""
INSERT INTO Therapy (PatientID, Note)
VALUES (?, ?)
""", ("PAT002", "Controllo pressorio settimanale"))

# ========== VERIFICA ==========

cursor.execute("SELECT * FROM Doctors")
print("Doctors:")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM Patients")
print("\nPatients:")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM Drugs")
print("\nDrugs:")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM Therapy")
print("\nTherapy:")
for row in cursor.fetchall():
    print(row)


start_date = datetime(2025, 5, 16).date()
end_date = datetime(2025, 6, 16).date()

slot_times = [  # Slot da 1h, dalle 08:30 alle 17:30
    "08:30", "09:30", "10:30", "11:30", "12:30",
    "13:30", "14:30", "15:30", "16:30"
]

doctors = [
    ("DOC001", "Mario Rossi"),
    ("DOC002", "Anna Vincentelli")
]

appointments = []

current_date = start_date
while current_date <= end_date:
    if current_date.weekday() < 5:  # Solo lun-ven
        for doctor_id, doctor_name in doctors:
            for slot in slot_times:
                appointments.append((
                    current_date.isoformat(),
                    slot,
                    doctor_id,
                    doctor_name,
                    'available',
                    None,
                    None
                ))
    current_date += timedelta(days=1)

# Esempi di appuntamenti prenotati
booked_slots = [
    # (date, time, doctor_id, patient_id, patient_name)
    ("2025-05-19", "08:30", "DOC001", "PAT001", "Luca Bianchi"),
    ("2025-05-20", "10:30", "DOC002", "PAT002", "Lucia Garofalo"),
    ("2025-05-23", "13:30", "DOC001", "PAT001", "Luca Bianchi"),
    ("2025-06-03", "15:30", "DOC002", "PAT002", "Lucia Garofalo")
]

# Segna come prenotati quelli indicati sopra
for i, (date, time_slot, doc_id, pat_id, pat_name) in enumerate(booked_slots):
    appointments.append((date, time_slot, doc_id, 
                         "Mario Rossi" if doc_id == "DOC001" else "Anna Vincentelli",
                         'booked', pat_id, pat_name))

# Inserimento in database
cursor.executemany("""
    INSERT INTO Appointments (date, time, doctor_id, doctor_name, status, patient_id, patient_name)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", appointments)

print("\nAppointments table populated from 16 May to 16 June 2025.")

conn.commit()
conn.close()