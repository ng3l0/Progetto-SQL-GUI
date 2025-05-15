import customtkinter as ctk
import sqlite3 

class VisitView(ctk.CTk):
    def __init__(self, patient_id, patient_name):
        super().__init__()
        self.patient_id = patient_id
        self.patient_name = patient_name

        self.title("Visita")
        self.geometry("800x500")
        self.center_window()

        # Layout principale
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Nome paziente
        self.profile_label = ctk.CTkLabel(self.sidebar_frame, text=f"👤 {patient_name}", anchor="w", font=("Arial", 14, "bold"))
        self.profile_label.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")

        # Pulsante evidenziato Home
        self.home_button = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.show_home, width=140)
        self.home_button.grid(row=1, column=0, padx=10, pady=10)

        # Pulsante Visual Data
        self.visual_data_button = ctk.CTkButton(self.sidebar_frame, text="Visual Data", width=140, command=self.visual_data)
        self.visual_data_button.grid(row=2, column=0, padx=10, pady=10)

        # --- Area centrale ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#e6f0ff")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.main_frame.grid_rowconfigure((1, 2), weight=1)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)

        # Titolo centrale
        title = ctk.CTkLabel(self.main_frame, text="Visits", font=("Arial", 24, "bold"), text_color="#204080")
        title.grid(row=0, column=0, columnspan=2, pady=40)

        # Bottone "book visit"
        book_button = ctk.CTkButton(self.main_frame, text="Book a visit", width=150, fg_color="#9b59b6", command=self.book_visit)
        book_button.grid(row=1, column=0, padx=20)

        # Bottone "check appointment"
        check_button = ctk.CTkButton(self.main_frame, text="Check appointments", width=150, fg_color="#b76ba3", command=self.check_appointment)
        check_button.grid(row=1, column=1, padx=20)

        self.mainloop()

    def book_visit(self):
        print(f"[{self.patient_id}] Prenotazione visita...")

    def check_appointment(self):
        print(f"[{self.patient_id}] Controllo appuntamenti...")

    def visual_data(self):
        print("Visual Data clicked")

    def show_home(self):
        print("Home clicked")

    def center_window(self):
        w = 800
        h = 500
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

if __name__ == "__main__":
    VisitView(patient_id="PAT001", patient_name="Luca Bianchi")
