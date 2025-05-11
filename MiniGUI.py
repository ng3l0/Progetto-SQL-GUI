import customtkinter as ctk
import sqlite3

class DoctorLoginApp:
    def __init__(self):
        self.conn = sqlite3.connect("Database_proj.db")
        self.cursor = self.conn.cursor()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("E-Health | Doctor Login")
        self.root.geometry("420x320")

        self.setup_login()
        self.root.mainloop()

    def setup_login(self):
        self.login_frame = ctk.CTkFrame(self.root, width=400, height=300, corner_radius=10)
        self.login_frame.pack(pady=30)

        title = ctk.CTkLabel(self.login_frame, text="Doctor Login", font=("Arial", 20, "bold"))
        title.pack(pady=(10, 20))

        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Doctor ID", width=250)
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login, width=150)
        self.login_button.pack(pady=10)

        self.message_label = ctk.CTkLabel(self.login_frame, text="", font=("Arial", 12))
        self.message_label.pack(pady=(10, 0))

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
        self.dashboard.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(self.dashboard, text="Patients Overview", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        self.cursor.execute("SELECT Name, Surname, PatientID FROM Patients")
        patients = self.cursor.fetchall()

        for name, surname, pid in patients:
            btn = ctk.CTkButton(self.dashboard, text=f"{name} {surname}", width=250,
                                command=lambda p=pid: self.show_patient_info(p))
            btn.pack(pady=5)

    def show_patient_info(self, patient_id):
        info_window = ctk.CTkToplevel(self.root)
        info_window.title("Patient Info")
        info_window.geometry("500x450")

        ctk.CTkLabel(info_window, text=f"Patient ID: {patient_id}", font=("Arial", 14, "bold")).pack(pady=10)

        # DRUGS
        self.cursor.execute("SELECT Note, StartDate, EndDate FROM Drugs WHERE PatientID = ?", (patient_id,))
        drugs = self.cursor.fetchall()

        ctk.CTkLabel(info_window, text="Drugs:", font=("Arial", 13, "bold")).pack(pady=(10, 0))
        if drugs:
            for note, start, end in drugs:
                ctk.CTkLabel(info_window, text=f"{note} ({start} to {end})").pack()
        else:
            ctk.CTkLabel(info_window, text="No drugs registered.").pack()

        # THERAPY
        self.cursor.execute("SELECT Note FROM Therapy WHERE PatientID = ?", (patient_id,))
        therapies = self.cursor.fetchall()

        ctk.CTkLabel(info_window, text="Therapies:", font=("Arial", 13, "bold")).pack(pady=(20, 0))
        if therapies:
            for (note,) in therapies:
                ctk.CTkLabel(info_window, text=note).pack()
        else:
            ctk.CTkLabel(info_window, text="No therapy registered.").pack()

DoctorLoginApp()
