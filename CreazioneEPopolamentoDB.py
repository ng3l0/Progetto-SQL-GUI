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

# INDEXES
cursor.execute("""
CREATE TABLE IF NOT EXISTS Indexes (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PatientID TEXT NOT NULL,
    Date DATE,
    ValueAHI REAL,
    ValueODI REAL,
    MeanSpO2 REAL,
    MinSpO2 REAL,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);
""")

# ========== INSERIMENTI ==========

# Doctors
cursor.executemany("""
INSERT INTO Doctors (Name, Surname, doctorID, DoctorPassword, dateOfBirth, hospital, PhoneNumber)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", [
    ("Mario", "Rossi", "DOC001", "password123", "1980-01-01", "Ospedale San Giovanni", "1234567890"),
    ("Anna", "Vincentelli", "DOC002", "password345", "1970-01-01", "Ospedale Galeazzi", "1234567777"),
    ("Lorenzo", "Esposito", "DOC003", "pass789", "1985-06-15", "Ospedale Niguarda", "1234561111")
])

# Patients
cursor.executemany("""
INSERT INTO Patients (Name, Surname, dateOfBirth, height, weight, Age, Gender, Nationality, ClinicalHistory, PatientID, PatientPassword, PhoneNumber)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ("Luca", "Bianchi", "2000-05-15", 1.75, 70, 33, "M", "Italiano", "Nessuna", "PAT001", "password123", "1234567890"),
    ("Lucia", "Garofalo", "2004-06-15", 1.65, 60, 25, "F", "Italiano", "Nessuna", "PAT002", "345678", "1234567899"),
    ("Marco", "Verdi", "1992-03-22", 1.80, 85, 32, "M", "Italiano", "Asma lieve", "PAT003", "pass333", "1234562222")
])

# Patients_OK
cursor.execute("INSERT INTO Patients_OK (PatientID, Date, Days_since_last_OSA) VALUES (?, ?, ?)", ("PAT001", "2025-04-25", 9))

# Patients_Follow_up
cursor.execute("INSERT INTO Patients_Follow_up (PatientID, Date, Days_since_last_OSA) VALUES (?, ?, ?)", ("PAT002", "2025-04-26", 2))

# Drugs
cursor.executemany("""
INSERT INTO Drugs (PatientID, Note, StartDate, EndDate)
VALUES (?, ?, ?, ?)
""", [
    ("PAT001", "Paracetamolo 500mg 2 volte al giorno", "2025-04-20", "2025-04-27"),
    ("PAT002", "Ibuprofene al bisogno", "2025-04-21", "2025-04-25"),
    ("PAT003", "Salbutamolo spray 2 puff al bisogno", "2025-04-22", "2025-04-30")
])

# Therapy
cursor.executemany("""
INSERT INTO Therapy (PatientID, Note)
VALUES (?, ?)
""", [
    ("PAT001", "Monitoraggio continuo con eventuale follow-up dopo 10 giorni"),
    ("PAT002", "Controllo pressorio settimanale"),
    ("PAT003", "Controllo asma trimestrale")
])

# Indexes
cursor.executemany("""
INSERT INTO Indexes (PatientID, Date, ValueAHI, ValueODI, MeanSpO2, MinSpO2)
VALUES (?, ?, ?, ?, ?, ?)
""", [
    ("PAT001", "2025-04-20", 5.2, 4.1, 95.2, 88.5),
    ("PAT001", "2025-04-19", 6.0, 3.5, 96.0, 89.0),
    ("PAT001", "2025-04-19", 5.3, 4.1, 95.0, 87.0), 
    ("PAT001", "2025-04-19", 5.5, 4.0, 95.5, 90.0),
    ("PAT002", "2025-04-21", 12.4, 8.7, 92.0, 84.3),
    ("PAT003", "2025-04-22", 2.5, 1.8, 96.5, 90.0)
])

conn.commit()
conn.close()

