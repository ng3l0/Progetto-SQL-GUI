import customtkinter as ctk
import sqlite3

class DoctorLoginApp:
    def __init__(self):
        self.conn = sqlite3.connect("Database_proj.db")
        self.cursor = self.conn.cursor()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Doctor Login")
        self.root.geometry("400x300")

        self.setup_login()
        self.root.mainloop()

    def setup_login(self):
        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(pady=50)

        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Doctor ID")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.message_label = ctk.CTkLabel(self.login_frame, text="")
        self.message_label.pack()

    def login(self):
        doctor_id = self.email_entry.get()
        password = self.password_entry.get()

        self.cursor.execute("SELECT * FROM Doctors WHERE doctorID = ? AND DoctorPassword = ?", (doctor_id, password))
        result = self.cursor.fetchone()

        if result:
            self.message_label.configure(text="Login successful", text_color="green")
            self.show_dashboard()
        else:
            self.message_label.configure(text="Invalid credentials", text_color="red")

    def show_dashboard(self):
        self.login_frame.destroy()

        self.dashboard = ctk.CTkFrame(self.root)
        self.dashboard.pack(pady=10, fill="both", expand=True)

        title = ctk.CTkLabel(self.dashboard, text="Patients Overview", font=("Arial", 16))
        title.pack(pady=10)

        self.cursor.execute("SELECT Name, Surname, PatientID FROM Patients")
        patients = self.cursor.fetchall()

        for patient in patients:
            name, surname, pid = patient
            button = ctk.CTkButton(self.dashboard, text=f"{name} {surname}", command=lambda p=pid: self.show_patient_info(p))
            button.pack(pady=5)

    def show_patient_info(self, patient_id):
        info_window = ctk.CTkToplevel(self.root)
        info_window.title("Patient Info")
        info_window.geometry("500x400")

        label = ctk.CTkLabel(info_window, text=f"Patient ID: {patient_id}", font=("Arial", 14))
        label.pack(pady=10)

        self.cursor.execute("SELECT Note, StartDate, EndDate FROM Drugs WHERE PatientID = ?", (patient_id,))
        drugs = self.cursor.fetchall()

        drugs_label = ctk.CTkLabel(info_window, text="Drugs:", font=("Arial", 12, "bold"))
        drugs_label.pack()
        for drug in drugs:
            note, start, end = drug
            ctk.CTkLabel(info_window, text=f"{note} ({start} to {end})").pack()

        self.cursor.execute("SELECT Note FROM Therapy WHERE PatientID = ?", (patient_id,))
        therapies = self.cursor.fetchall()

        therapy_label = ctk.CTkLabel(info_window, text="Therapies:", font=("Arial", 12, "bold"))
        therapy_label.pack(pady=(10, 0))
        for therapy in therapies:
            ctk.CTkLabel(info_window, text=therapy[0]).pack()

DoctorLoginApp()
