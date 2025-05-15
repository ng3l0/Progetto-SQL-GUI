import sqlite3
import customtkinter as ctk

class PatientMainView(ctk.CTk):
    def __init__(self, patient_id):
        super().__init__()

        self.patient_id = patient_id
        self.patient_name = self.get_patient_name(patient_id)
        self.initialize_questionnaire_table()

        self.title(f"Patient Dashboard - {self.patient_name}")
        self.geometry("800x500")

        # layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ----- Sidebar -----
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.profile_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {self.patient_name}", font=("Arial", 14, "bold"))
        self.profile_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.show_home, width=140)
        self.home_button.grid(row=1, column=0, padx=10, pady=10)

        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", command=self.show_visual_data, width=140)
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        # ----- Main content -----
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#e6f0ff")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.show_home()

        self.mainloop()

    def initialize_questionnaire_table(self):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS QuestionnaireStatus (
                PatientID TEXT PRIMARY KEY,
                Done INTEGER DEFAULT 0,
                FOREIGN KEY(PatientID) REFERENCES Patients(PatientID)
            )
        """)
        conn.commit()
        conn.close()
            
    def is_questionnaire_done(self, patient_id):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Done FROM QuestionnaireStatus WHERE PatientID = ?", (patient_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] == 1 if result else False
    
    def toggle_questionnaire_status(self):
        new_status = 1 if not self.questionnaire_done else 0
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO QuestionnaireStatus (PatientID, Done) VALUES (?, ?)", 
                    (self.patient_id, new_status))
        conn.commit()
        conn.close()

        self.questionnaire_done = bool(new_status)
        self.show_home()  # per aggiornare la UI
        if new_status == 1:
        # Dopo 2 secondi (2000 ms), resetta
            self.after(2000, self.reset_questionnaire_status)

    def reset_questionnaire_status(self):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE QuestionnaireStatus SET Done = 0 WHERE PatientID = ?", (self.patient_id,))
        conn.commit()
        conn.close()

        self.questionnaire_done = False
        self.show_home()  # aggiorna la UI


    #def is_questionnaire_done(self, patient_id):
     #   conn = sqlite3.connect("Database_proj.db")
     #   cursor = conn.cursor()
      #  cursor.execute("SELECT QuestionnaireDone FROM Patients WHERE PatientID = ?", (patient_id,))
      #  result = cursor.fetchone()
     #   conn.close()
      #  return result[0] == 1 if result else False

    def show_home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.questionnaire_done = self.is_questionnaire_done(self.patient_id)  # aggiorna stato da DB

        title = ctk.CTkLabel(
            self.main_frame,
            text="Welcome to your Patient Portal",
            font=("Arial", 22, "bold"),
            text_color="#204080" 
            )
        title.pack(pady=20)

        # Buttons area
        questionnaire_text = "Questionnaire" + (" ✔️" if self.questionnaire_done else "")
        questionnaire_color = "green" if self.questionnaire_done else "blue"
        questionnaire_state = "normal"

        self.questionnaire_button = ctk.CTkButton(
            self.main_frame,
            text=questionnaire_text,
            fg_color=questionnaire_color,
            width=250,
            command=self.toggle_questionnaire_status,  # <-- assicurati che punti qui
            state=questionnaire_state
        )
        self.questionnaire_button.pack(pady=15)

        self.visits_button = ctk.CTkButton(self.main_frame, text="Visits", width=250,
                                           command=self.open_visits)
        self.visits_button.pack(pady=15)

        self.medication_button = ctk.CTkButton(self.main_frame, text="Medication", width=250,
                                               command=self.open_medication)
        self.medication_button.pack(pady=15)

    def show_visual_data(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        title = ctk.CTkLabel(
            self.main_frame, text="Visual Data (coming soon)",             
            font=("Arial", 22, "bold"),
            text_color="#204080" 
            
            )
        title.pack(pady=20)

    def open_questionnaire(self):
        print("Open Questionnaire window")  # da collegare

    def open_visits(self):
        print("Open Visits window")  # da collegare

    def open_medication(self):
        print("Open Medication window")  # da collegare

    def get_patient_name(self, patient_id):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Name, Surname FROM Patients WHERE PatientID = ?", (patient_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return f"{result[0]} {result[1]}"
        else:
            return "Unknown Patient"

# Test locale
if __name__ == "__main__":
    PatientMainView(patient_id="PAT001")
