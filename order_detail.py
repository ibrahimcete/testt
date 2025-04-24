import customtkinter as ctk
from tkinter import messagebox

class OrderDetail(ctk.CTkFrame):
    def __init__(self, master, trendyol_client):
        super().__init__(master)
        self.trendyol_client = trendyol_client
        self.configure(fg_color="white", corner_radius=10)
        ctk.CTkLabel(self, text="Sipariş Detayları", font=("Roboto", 24, "bold"), text_color="#1E293B").pack(padx=20, pady=20)
        ctk.CTkLabel(self, text="Sipariş ID:", font=("Roboto", 14), text_color="black").pack(pady=(10,0))
        self.order_id_entry = ctk.CTkEntry(self, font=("Roboto", 14), width=250)
        self.order_id_entry.pack()
        ctk.CTkButton(self, text="Detayları Göster", command=self.show_order_detail).pack(pady=10)
        self.details_box = ctk.CTkTextbox(self, width=800, height=300)
        self.details_box.pack(padx=20, pady=10)

    def show_order_detail(self):
        order_id = self.order_id_entry.get().strip()
        self.details_box.delete("1.0", "end")
        if not order_id.isdigit():
            self.details_box.insert("1.0", "Geçersiz ID")
            return
        try:
            detail = self.trendyol_client.get_order_detail(int(order_id))
            self.details_box.insert("1.0", str(detail))
        except Exception as e:
            messagebox.showerror("Hata", f"Sipariş detayı alınamadı: {str(e)}")