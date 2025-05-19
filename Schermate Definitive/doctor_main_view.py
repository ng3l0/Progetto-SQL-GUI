import customtkinter
import os
from PIL import Image
import sqlite3
import tkinter.ttk as ttk
from OSA_Patients import OSAPatientsView  


class DoctorMainView(customtkinter.CTk):
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
        self.sidebar = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_rowconfigure(6, weight=1)

        self.doctor_label = customtkinter.CTkLabel(self.sidebar, text=f"🧑‍⚕️ {self.doctor_name}", font=("Arial", 16, "bold"))
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
            btn = customtkinter.CTkButton(
                self.sidebar, text=text, height=40,
                command=lambda c=command: self.switch_main_view(c),
                fg_color="transparent", hover_color="#d9d9d9", corner_radius=0
            )
            btn.grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")

        # buttons_text = ["OSA patients", "Follow up patients", "Possible Follow up", "New Therapy", "Visits"]
        # for i, txt in enumerate(buttons_text):
        #      color = "#204080" if txt == "OSA patients" else "transparent" #colore casella selezionata
        #      btn = customtkinter.CTkButton(self.sidebar, text=txt, height=40, fg_color=color,
        #                                    hover_color="#e0e0e0", corner_radius=0)
        #      btn.grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")
       

        # Main content
        self.main_view = customtkinter.CTkFrame(self, fg_color="#e6f0ff")
        self.main_view.grid(row=0, column=1, sticky="nsew")
        self.main_view.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Carica vista iniziale
        self.switch_main_view(self.go_to_OSA_Patients)

    def switch_main_view(self, content_function):
        for widget in self.main_view.winfo_children():
            widget.destroy()
        content_function()

        # title = customtkinter.CTkLabel(self.main_view, text="OSA patients", font=("Arial", 20, "bold"), text_color="black")
        # title.grid(row=0, column=0, columnspan=4, pady=20)

        # # Recupera dati dal database
        # columns, data = self.get_osa_patients()

        # # Treeview style (facoltativo, per renderla un po' più carina)
        # style = ttk.Style()
        # style.theme_use("default")
        # style.configure("Treeview", background="#f0f4ff", foreground="black", rowheight=25, fieldbackground="#f0f4ff")
        # style.map("Treeview", background=[('selected', '#4a7abc')])

        # # Crea la tabella Treeview
        # self.tree = ttk.Treeview(self.main_view, columns=columns, show='headings', height=12)
        # self.tree.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        # # Inserisci le intestazioni
        # for col in columns:
        #      self.tree.heading(col, text=col)
        #      self.tree.column(col, anchor="center", width=100)

        # # Inserisci i dati
        # for row in data:
        #      self.tree.insert("", "end", values=row)
    def get_osa_patients(self):
            conn = sqlite3.connect("Database_proj.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM OSA_Patients")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            conn.close()
            return column_names, rows

    def get_doctor_name(self, user_id) :
            conn = sqlite3.connect("Database_proj.db")
            cursor = conn.cursor()
            cursor.execute("SELECT Name, Surname FROM Doctors WHERE doctorID = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()
            return f"{result[0]} {result[1]}" if result else "Unknown Doctor"

    

    def go_to_OSA_Patients(self):
            from OSA_Patients import OSAPatientsView  # attenzione al nome file!
            OSAPatientsView (self.main_view, self.user_id)

    def go_to_possible_follow_up(self):
            from Possible_Follow_Up_Patients import PossibleFollowUpPatientsView # attenzione al nome file!
            PossibleFollowUpPatientsView(self.main_view, self.user_id)

    def go_to_follow_up(self):
            from Follow_Up_Patients import FollowUpPatientsView
            FollowUpPatientsView(self.main_view, self.user_id)
    
    def go_to_visits(self):
            from OSA_Patients import OSAPatientsView # attenzione al nome file!
            OSAPatientsView(user_id=self.user_id)

    def go_to_7_days_ok(self):
            from Seven_Days_ok_patients import Seven_Days_Ok_PatientsView# attenzione al nome file!
            Seven_Days_Ok_PatientsView(self.main_view, self.user_id)

if __name__ == "__main__":
    app = DoctorMainView(user_id= "DOC001")
    app.mainloop()