import customtkinter as ctk
from tkinter import messagebox

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, login_callback):
        super().__init__(master)
        self.login_callback = login_callback
        self.configure(fg_color="white", corner_radius=10)
        ctk.CTkLabel(self, text="Giriş", font=("Roboto", 28, "bold"), text_color="#1E293B").pack(pady=20)
        ctk.CTkLabel(self, text="Kullanıcı Adı:", font=("Roboto", 14), text_color="black").pack(pady=(10,0))
        self.username = ctk.CTkEntry(self, font=("Roboto", 14), width=250)
        self.username.pack()
        ctk.CTkLabel(self, text="Şifre:", font=("Roboto", 14), text_color="black").pack(pady=(10,0))
        self.password = ctk.CTkEntry(self, font=("Roboto", 14), show="*", width=250)
        self.password.pack()
        ctk.CTkButton(self, text="Giriş Yap", command=self.try_login, fg_color="#00C49F").pack(pady=20)

    def try_login(self):
        user = self.username.get().strip()
        pw = self.password.get().strip()
        if user == "admin" and pw == "admin":  # Basit demo giriş kontrolü
            self.login_callback(user)
        else:
            messagebox.showerror("Hatalı giriş", "Kullanıcı adı ya da şifre hatalı")