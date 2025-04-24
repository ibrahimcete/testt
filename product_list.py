import customtkinter as ctk
from tkinter import messagebox

class ProductList(ctk.CTkFrame):
    def __init__(self, master, trendyol_client):
        super().__init__(master)
        self.trendyol_client = trendyol_client
        self.configure(fg_color="white", corner_radius=10)
        ctk.CTkLabel(self, text="Ürün Listesi", font=("Roboto", 24, "bold"), text_color="#1E293B").pack(padx=20, pady=20)
        self.listbox = ctk.CTkTextbox(self, width=800, height=400)
        self.listbox.pack(padx=20, pady=10)
        ctk.CTkButton(self, text="Yenile", command=self.refresh_products).pack()
        self.refresh_products()

    def refresh_products(self):
        self.listbox.delete("1.0", "end")
        try:
            products = self.trendyol_client.get_products()
            content = products.get("content", [])
            if not content:
                self.listbox.insert("1.0", "Ürün bulunamadı.")
                return
            for p in content:
                self.listbox.insert("end", f"ID: {p.get('id')} | {p.get('title', '???')} | Fiyat: {p.get('price', '???')} | Stok: {p.get('stock', '???')}\n")
        except Exception as e:
            messagebox.showerror("Hata", f"Ürünler alınamadı: {str(e)}")