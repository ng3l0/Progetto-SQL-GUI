import customtkinter as ctk
import sqlite3
import os
from PIL import Image
import tkinter.ttk as ttk
from patient_main_view import PatientMainView
from doctor_main_view import DoctorMainView

class AppProg:
    def __init__(self):
        self.user = ""
        self.conn = sqlite3.connect("Database_proj.db")
        self.cursor = self.conn.cursor()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("E-Health | Login")
        self.root.geometry("420x320")

        self.setup_login()
        self.root.mainloop()

    def setup_login(self):
        self.login_frame = ctk.CTkFrame(self.root, width=400, height=300, corner_radius=10)
        self.login_frame.pack(pady=30)

        title = ctk.CTkLabel(self.login_frame, text="Login", font=("Arial", 20, "bold"))
        title.pack(pady=(10, 20))

        self.role_option = ctk.CTkOptionMenu(self.login_frame, values=["Doctor", "Patient"])
        self.role_option.set("Doctor")  # Default
        self.role_option.pack(pady=10)

        self.email_entry = ctk.CTkEntry(self.login_frame, placeholder_text="ID", width=250)
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login, width=150)
        self.login_button.pack(pady=10)

        self.message_label = ctk.CTkLabel(self.login_frame, text="", font=("Arial", 12))
        self.message_label.pack(pady=(10, 0))

    def go_to_home_doctor(self):
        from doctor_main_view import DoctorMainView
        self.root.destroy()  # sposta qui la distruzione
        DoctorMainView(self, self.user_id)

    def go_to_home_patient(self):
        from patient_main_view import PatientMainView
        self.root.destroy()
        PatientMainView(self, self.user_id)


    def login(self):
       user_id = self.email_entry.get()             # Legge l'ID inserito
       password = self.password_entry.get()         # Legge la password
       role = self.role_option.get()                # Legge se ha selezionato "Doctor" o "Patient"

       if role == "Doctor":
            # Query nella tabella Doctors
            self.cursor.execute(
                "SELECT * FROM Doctors WHERE doctorID = ? AND DoctorPassword = ?", 
                (user_id, password)
            )
            result = self.cursor.fetchone()
            
            if result:
                self.user_id = user_id
                self.message_label.configure(text="Doctor login successful", text_color="green")
                self.go_to_home_doctor()
            else:
                self.message_label.configure(text="Invalid doctor credentials", text_color="red")

       elif role == "Patient":
            # Query nella tabella Patients
            self.cursor.execute(
                "SELECT * FROM Patients WHERE ID = ? AND PatientPassword = ?", 
                (user_id, password)
            )
            result = self.cursor.fetchone()

            if result:
                self.user_id = user_id
                self.message_label.configure(text="Patient login successful", text_color="green")
                self.go_to_home_patient()  # Create and show the patient dashboard

            else:
                self.message_label.configure(text="Invalid patient credentials", text_color="red")


AppProg()


