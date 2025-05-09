import sqlite3

conn = sqlite3.connect("Database_proj.db")
cursor = conn.cursor()

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

# ========== INSERIMENTI ==========

# Doctors
cursor.execute("""
INSERT INTO Doctors (Name, Surname, doctorID, DoctorPassword, dateOfBirth, hospital, PhoneNumber)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", ("Mario", "Rossi", "DOC001", "password123", "1980-01-01", "Ospedale San Giovanni", "1234567890"))

cursor.execute("""
INSERT INTO Doctors (Name, Surname, doctorID, DoctorPassword, dateOfBirth, hospital, PhoneNumber)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", ("Anna", "Vincentelli", "DOC002", "password345", "1970-01-01", "Ospedale Galeazzi", "1234567777"))

# Patients
cursor.execute("""
INSERT INTO Patients (Name, Surname, dateOfBirth, height, weight, Age, Gender, Nationality, ClinicalHistory, PatientID, PatientPassword, PhoneNumber)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ("Luca", "Bianchi", "2000-05-15", 1.75, 70, 33, "M", "Italiano", "Nessuna", "PAT001", "password123", "1234567890"))

cursor.execute("""
INSERT INTO Patients (Name, Surname, dateOfBirth, height, weight, Age, Gender, Nationality, ClinicalHistory, PatientID, PatientPassword, PhoneNumber)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ("Lucia", "Garofalo", "2004-06-15", 1.65, 60, 25, "F", "Italiano", "Nessuna", "PAT002", "345678", "1234567899"))

# Patients_OK
cursor.execute("""
INSERT INTO Patients_OK (PatientID, Date, Days_since_last_OSA)
VALUES (?, ?, ?)
""", ("PAT001", "2025-04-25", 9))

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

conn.commit()
conn.close()
