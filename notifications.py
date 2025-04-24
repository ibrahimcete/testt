import customtkinter as ctk

class Notifications(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="white", corner_radius=10)
        ctk.CTkLabel(self, text="Bildirimler", font=("Roboto", 24, "bold"), text_color="#1E293B").pack(padx=20, pady=20)
        self.notifications_list = ctk.CTkTextbox(self, width=500, height=300)
        self.notifications_list.pack(padx=20, pady=10)
        self.load_notifications()

    def load_notifications(self):
        notifications = [
            "Yeni sipariş: 12345",
            "Ürün güncellendi: Ürün ABC",
            "Rapor hazırlandı: Günlük satış raporu"
        ]
        self.notifications_list.delete("1.0", "end")
        self.notifications_list.insert("1.0", "\n".join(notifications))