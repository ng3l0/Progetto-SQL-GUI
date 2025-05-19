import customtkinter as ctk
import os
from PIL import Image
import sqlite3
import tkinter.ttk as ttk
import datetime

class DoctorMainView(ctk.CTk):
    def __init__(self, user_id):
        super().__init__()
        
        self.user_id = user_id
        self.doctor_name = self.get_doctor_name(user_id)

        self.title("Doctor Main View")
        self.geometry("900x500")

        # Layout setup
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_rowconfigure(6, weight=1)

        self.doctor_label = ctk.CTkLabel(self.sidebar, text=f"🧑‍⚕️ {self.doctor_name}", font=("Arial", 16, "bold"))
        self.doctor_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Bottoni sidebar
        buttons = [
            ("OSA patients", self.go_to_OSA_Patients),
            ("Follow up patients", self.go_to_follow_up),
            ("Possible Follow up", self.go_to_possible_follow_up),
            ("7 Days OK Patients ", self.go_to_7_days_ok),
            ("Visits", self.go_to_visits),
        ]
        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                self.sidebar, text=text, height=40,
                command=lambda c=command: self.switch_main_view(c),
                fg_color="transparent", hover_color="#d9d9d9", corner_radius=0
            )
            btn.grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")

        # Main content
        self.main_view = ctk.CTkFrame(self, fg_color="#e6f0ff")
        self.main_view.grid(row=0, column=1, sticky="nsew")
        self.main_view.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Carica vista iniziale
        self.switch_main_view(self.go_to_OSA_Patients)

    def switch_main_view(self, content_function):
        for widget in self.main_view.winfo_children():
            widget.destroy()
        content_function()

    def get_osa_patients(self):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM OSA_Patients")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()
        return column_names, rows

    def get_doctor_name(self, user_id):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Name, Surname FROM Doctors WHERE doctorID = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return f"{result[0]} {result[1]}" if result else "Unknown Doctor"

    def go_to_OSA_Patients(self):
        try:
            from OSA_Patients import OSAPatientsView
            OSAPatientsView(self.main_view, self.user_id)
        except Exception as e:
            print(f"Error loading OSA patients view: {e}")

    def go_to_possible_follow_up(self):
        try:
            from Possible_Follow_Up_Patients import PossibleFollowUpPatientsView
            PossibleFollowUpPatientsView(self.main_view, self.user_id)
        except Exception as e:
            print(f"Error loading possible follow up view: {e}")

    def go_to_follow_up(self):
        try:
            from Follow_Up_Patients import FollowUpPatientsView
            FollowUpPatientsView(self.main_view, self.user_id)
        except Exception as e:
            print(f"Error loading follow up view: {e}")
    
    def go_to_visits(self):
        try:
            from VisitDoctorView import VisitDoctorView
            VisitDoctorView(self.main_view, self.user_id)
        except Exception as e:
            print(f"Error loading visits view: {e}")

    def go_to_7_days_ok(self):
        try:
            from Seven_Days_ok_patients import Seven_Days_Ok_PatientsView
            Seven_Days_Ok_PatientsView(self.main_view, self.user_id)
        except Exception as e:
            print(f"Error loading 7 days ok view: {e}")

if __name__ == "__main__":
    app = DoctorMainView(user_id="DOC001")
    app.mainloop()