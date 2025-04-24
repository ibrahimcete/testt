import customtkinter as ctk
from tkinter import messagebox

class UserManagement(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white", corner_radius=10)
        ctk.CTkLabel(self, text="Kullanıcı Yönetimi", font=("Roboto", 24, "bold"), text_color="#1E293B").pack(padx=20, pady=20)
        self.users_box = ctk.CTkTextbox(self, width=500, height=300)
        self.users_box.pack(padx=20, pady=10)
        self.load_users()

    def load_users(self):
        # Demo kullanıcı listesi
        users = [
            "admin (Yönetici)",
            "ali (Kullanıcı)",
            "ayse (Kullanıcı)"
        ]
        self.users_box.delete("1.0", "end")
        self.users_box.insert("1.0", "\n".join(users))