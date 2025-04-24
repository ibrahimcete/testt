import customtkinter as ctk
from tkinter import messagebox

class Reports(ctk.CTkFrame):
    def __init__(self, master, trendyol_client):
        super().__init__(master)
        self.trendyol_client = trendyol_client
        self.configure(fg_color="white", corner_radius=10)
        ctk.CTkLabel(self, text="Raporlar", font=("Roboto", 24, "bold"), text_color="#1E293B").pack(padx=20, pady=20)
        ctk.CTkButton(self, text="Rapor Oluştur", command=self.generate_report).pack(padx=20, pady=10)
        self.report_text = ctk.CTkTextbox(self, width=800, height=400)
        self.report_text.pack(padx=20, pady=10)

    def generate_report(self):
        try:
            products = self.trendyol_client.get_products()
            orders = self.trendyol_client.get_orders(start_date="2025-01-01", end_date="2025-12-31")
            report_content = f"Ürün Sayısı: {len(products.get('content', []))}\n"
            report_content += f"Sipariş Sayısı: {len(orders.get('content', []))}\n"
            self.report_text.delete("1.0", "end")
            self.report_text.insert("1.0", report_content)
        except Exception as e:
            messagebox.showerror("Rapor Hatası", f"Rapor oluşturulurken hata: {str(e)}")