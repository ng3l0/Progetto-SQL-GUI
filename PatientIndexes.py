import customtkinter as ctk

class PatientIndexes(ctk.CTk):
    def __init__(self, patient_id, patient_name="Unknown Patient"):
        super().__init__()

        self.patient_id = patient_id
        self.patient_name = patient_name

        self.title(f"Patient Indexes - {self.patient_name}")
        self.geometry("800x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ----- Sidebar -----
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.profile_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {self.patient_name}", font=("Arial", 14, "bold"))
        self.profile_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.go_home, width=140)
        self.home_button.grid(row=1, column=0, padx=10, pady=10)

        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", width=140, state="disabled")
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        # ----- Main Frame -----
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#e6f0ff")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.show_indexes()

        self.mainloop()

    def show_indexes(self):
        title = ctk.CTkLabel(self.main_frame, text="Select an Index to View", font=("Arial", 18, "bold"), text_color="#204080")
        title.pack(pady=30)

        # AHI button (lilac)
        self.ahi_button = ctk.CTkButton(self.main_frame, text="AHI", width=200, fg_color="#c8b4e3", hover_color="#b39ddb", command=self.open_ahi)
        self.ahi_button.pack(pady=15)

        # ODI button (beige)
        self.odi_button = ctk.CTkButton(self.main_frame, text="ODI", width=200, fg_color="#e0cda9", hover_color="#d2b48c", command=self.open_odi)
        self.odi_button.pack(pady=15)

        # SpO2 button (green)
        self.spo2_button = ctk.CTkButton(self.main_frame, text="SpO2", width=200, fg_color="#a8d5ba", hover_color="#81c784", command=self.open_spo2)
        self.spo2_button.pack(pady=15)

    def go_home(self):
        print("Back to home")  # Placeholder, link to PatientMainView

    def open_ahi(self):
        print(f"Open AHI screen for {self.patient_id}")

    def open_odi(self):
        print(f"Open ODI screen for {self.patient_id}")

    def open_spo2(self):
        print(f"Open SpO2 screen for {self.patient_id}")

# Test locale
if __name__ == "__main__":
    PatientIndexes(patient_id="PAT001", patient_name="Luca Bianchi")