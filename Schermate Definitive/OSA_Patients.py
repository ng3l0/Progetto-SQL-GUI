import customtkinter as ctk
import os
from PIL import Image
import sqlite3
import tkinter.ttk as ttk

class OSAPatientsView(ctk.CTkFrame):
    def __init__(self, parent_frame, user_id):
        super().__init__(parent_frame)
        self.user_id = user_id
        
        # Titolo
        title = ctk.CTkLabel(self, text="OSA patients", font=("Arial", 20, "bold"), text_color="black")
        title.grid(row=0, column=0, columnspan=4, pady=20)

        # Recupera dati dal database
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM OSA_Patients")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()

        # Treeview style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#f0f4ff", foreground="black", rowheight=25, fieldbackground="#f0f4ff")
        style.map("Treeview", background=[('selected', '#4a7abc')])

        # Tabella
        self.tree = ttk.Treeview(self, columns=column_names, show='headings', height=12)
        self.tree.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        for col in column_names:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)

        for row in rows:
            self.tree.insert("", "end", values=row)

    def get_osa_patients(self):
        conn = sqlite3.connect("Database_proj.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM OSA_Patients")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()
        return column_names, rows


if __name__ == "__main__":
    app = OSAPatientsView(user_id=1)  # oppure un altro id valido
    app.mainloop()

