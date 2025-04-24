import customtkinter as ctk
from tkinter import messagebox, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, trendyol_client):
        super().__init__(master)
        self.trendyol_client = trendyol_client
        self.configure(fg_color="white")
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)

        # ÜST BİLGİLENDİRME KARTLARI
        self.create_info_cards()

        # SATIŞ GRAFİĞİ + TARİH FİLTRESİ
        self.create_sales_graph()

        # EN ÇOK SATANLAR KARTLARI
        self.create_best_sellers()

        # UYARILAR
        self.create_alert_cards()

        # GÜNLÜK FİNANSAL KART
        self.create_daily_finance()

        # BİLDİRİMLER
        self.create_notifications()

        # SİPARİŞ LİSTESİ (API'den)
        self.create_order_list_section()

    def create_info_cards(self):
        card_data = [
            ("Trendyol", 5, "#24C38C", "🛒"),
            ("N11", 3, "#30A9E1", "🏪"),
            ("Hepsiburada", 8, "#A259FF", "🏬"),
        ]
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.grid(row=0, column=0, sticky="nwe", padx=20, pady=(10,5), columnspan=2)
        for i, (title, value, color, icon) in enumerate(card_data):
            card = ctk.CTkFrame(frame, fg_color=color, corner_radius=12, width=160, height=70)
            card.grid(row=0, column=i, padx=10, pady=5)
            ctk.CTkLabel(card, text=f"{icon}", font=("Arial", 18, "bold"), text_color="white").place(x=10, y=8)
            ctk.CTkLabel(card, text=title, font=("Arial", 14, "bold"), text_color="white").place(x=45, y=8)
            ctk.CTkLabel(card, text=f"{value}", font=("Arial", 24, "bold"), text_color="white").place(x=45, y=32)

    def create_sales_graph(self):
        graph_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=14)
        graph_frame.grid(row=1, column=0, sticky="nwes", padx=20, pady=10, rowspan=2)
        graph_frame.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(graph_frame, text="Son 7 Günlük Satış Grafiği", font=("Arial", 18, "bold"), text_color="#222").grid(row=0, column=0, sticky="w", padx=20, pady=(10,2))
        self.date_filter = ctk.CTkOptionMenu(graph_frame, values=["Bugün", "Hafta", "Ay"], command=self.refresh_graph)
        self.date_filter.set("Hafta")
        self.date_filter.grid(row=0, column=1, sticky="e", padx=20, pady=(10,2))
        self.fig, self.ax = plt.subplots(figsize=(6,3), dpi=90)
        self.sales_days = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        self.sales_data = [3, 5, 2, 7, 4, 8, 6]
        self.bar = self.ax.bar(self.sales_days, self.sales_data, color="#24C38C")
        self.ax.set_ylabel("Adet")
        self.ax.set_title("Satışlar")
        self.ax.grid(axis="y", linestyle="--", alpha=0.3)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky="nwe", padx=10, pady=10)
        self.canvas.draw()
        self.canvas.mpl_connect("motion_notify_event", self.on_graph_hover)

    def refresh_graph(self, selected_range):
        if selected_range == "Bugün":
            y = [2]
            x = ["Bugün"]
        elif selected_range == "Hafta":
            x = self.sales_days
            y = self.sales_data
        else:
            x = [f"{i+1}.gün" for i in range(30)]
            y = [i%7+1 for i in range(30)]
        self.ax.clear()
        self.bar = self.ax.bar(x, y, color="#24C38C")
        self.ax.set_ylabel("Adet")
        self.ax.set_title("Satışlar")
        self.ax.grid(axis="y", linestyle="--", alpha=0.3)
        self.canvas.draw()

    def on_graph_hover(self, event):
        if event.inaxes == self.ax:
            for bar in self.bar:
                if bar.contains(event)[0]:
                    idx = self.bar.index(bar)
                    val = self.bar[idx].get_height()
                    self.ax.set_title(f"Gün: {self.sales_days[idx]}  | Satış: {val} adet")
                    self.canvas.draw()
                    return
            self.ax.set_title("Satışlar")
            self.canvas.draw()

    def create_best_sellers(self):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.grid(row=1, column=1, sticky="nwe", padx=10, pady=10)
        ctk.CTkLabel(frame, text="En Çok Satan Ürünler", font=("Arial", 16, "bold"), text_color="#333").pack(anchor="w", padx=10, pady=(5,5))
        bests = [("Ürün A", 50), ("Ürün B", 35), ("Ürün C", 20)]
        kutu_renk = ["#EFFAF3", "#E7F3FA", "#F3EEFA"]
        for i, (urun, adet) in enumerate(bests):
            card = ctk.CTkFrame(frame, fg_color=kutu_renk[i], corner_radius=10, width=200, height=45)
            card.pack(fill="x", padx=6, pady=5)
            ctk.CTkLabel(card, text=f"{urun}", font=("Arial", 13, "bold"), text_color="#222").place(x=10, y=6)
            ctk.CTkLabel(card, text=f"{adet} adet", font=("Arial", 13, "bold"), text_color="#666").place(x=120, y=6)

    def create_alert_cards(self):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.grid(row=3, column=0, sticky="w", padx=20, pady=(5,10))
        red_card = ctk.CTkFrame(frame, fg_color="#FF6B6B", corner_radius=8)
        red_card.pack(side="left", padx=6, pady=6)
        ctk.CTkLabel(red_card, text="❗ 2 sipariş kargolanmadı!", font=("Arial", 13, "bold"), text_color="white").pack(padx=18, pady=6)
        yellow_card = ctk.CTkFrame(frame, fg_color="#FFE066", corner_radius=8)
        yellow_card.pack(side="left", padx=6, pady=6)
        ctk.CTkLabel(yellow_card, text="⚠️ API bağlantısı kopmuş!", font=("Arial", 13, "bold"), text_color="#B58900").pack(padx=18, pady=6)

    def create_daily_finance(self):
        frame = ctk.CTkFrame(self, fg_color="#24C38C", corner_radius=10)
        frame.grid(row=3, column=1, sticky="e", padx=10, pady=(5,10))
        ctk.CTkLabel(frame, text="Günlük Ciro: 1500 TL", font=("Arial", 15, "bold"), text_color="white").pack(padx=15, pady=(8,2), anchor="w")
        ctk.CTkLabel(frame, text="Kâr: 300 TL", font=("Arial", 13, "bold"), text_color="white").pack(padx=15, pady=(2,8), anchor="w")

    def create_notifications(self):
        frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10, width=300, height=220)
        frame.place(relx=1.0, rely=1.0, anchor="se", x=-25, y=-25)
        head_frame = ctk.CTkFrame(frame, fg_color="white")
        head_frame.pack(fill="x", padx=6, pady=(6,0))
        ctk.CTkLabel(head_frame, text="Bildirimler", font=("Arial", 14, "bold"), text_color="#1E293B").pack(side="left")
        ctk.CTkButton(head_frame, text="Tüm Bildirimler", width=90, fg_color="#24C38C", command=self.open_all_notifications).pack(side="right", padx=3)
        notif_box = ctk.CTkScrollableFrame(frame, fg_color="#F3F8F7", corner_radius=8, height=135)
        notif_box.pack(fill="both", padx=7, pady=(3,10), expand=True)
        notifications = [
            "Yeni sipariş: #12345",
            "Kargo bilgisi güncellendi",
            "Ürün stoğunuz azaldı",
            "API bağlantısı tekrar sağlandı",
            "Yeni yorum: 5 yıldız!"
        ]
        for notif in notifications[:5]:
            ctk.CTkLabel(notif_box, text=notif, font=("Arial", 12), text_color="#222", anchor="w").pack(anchor="w", padx=8, pady=2)

    def open_all_notifications(self):
        win = Toplevel(self)
        win.title("Tüm Bildirimler")
        win.geometry("400x500")
        notif_box = ctk.CTkScrollableFrame(win, fg_color="white", corner_radius=10)
        notif_box.pack(fill="both", expand=True, padx=18, pady=18)
        notifications = [
            "Yeni sipariş: #12345",
            "Kargo bilgisi güncellendi",
            "Ürün stoğunuz azaldı",
            "API bağlantısı tekrar sağlandı",
            "Yeni yorum: 5 yıldız!"
        ] * 4
        for notif in notifications:
            ctk.CTkLabel(notif_box, text=notif, font=("Arial", 12), anchor="w", text_color="#222").pack(anchor="w", padx=10, pady=3)

    def create_order_list_section(self):
        # Siparişleri gösteren scrollable tablo
        self.orders_frame = ctk.CTkFrame(self, fg_color="white")
        self.orders_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))
        ctk.CTkLabel(self.orders_frame, text="Trendyol Siparişleri", font=("Arial", 15, "bold")).pack(anchor="w", pady=(5,2), padx=6)
        ctk.CTkButton(self.orders_frame, text="Siparişleri API'den Çek", fg_color="#24C38C", command=self.update_orders).pack(side="right", padx=8, pady=6)
        self.orders_table = ctk.CTkScrollableFrame(self.orders_frame, fg_color="#FAFBFD", height=200, corner_radius=8)
        self.orders_table.pack(fill="both", expand=True, padx=3, pady=3)
        self.render_orders([])

    def update_orders(self):
        try:
            orders = self.trendyol_client.get_orders()
            self.render_orders(orders)
            messagebox.showinfo("Başarılı", f"{len(orders)} adet sipariş başarıyla çekildi.")
        except Exception as e:
            messagebox.showerror("API Hatası", f"Siparişler çekilemedi:\n{e}")

    def render_orders(self, orders):
        for widget in self.orders_table.winfo_children():
            widget.destroy()
        # Başlık
        header = ["Sipariş No", "Alıcı", "Ürünler", "Adet", "Durum"]
        for i, h in enumerate(header):
            ctk.CTkLabel(self.orders_table, text=h, font=("Arial", 12, "bold"), text_color="#222", width=120).grid(row=0, column=i, padx=2, pady=2)
        # Satırlar
        for idx, order in enumerate(orders):
            order_id = order.get("id", "")
            customer = order.get("customerFirstName", "") + " " + order.get("customerLastName", "")
            lines = order.get("lines", [])
            products = ", ".join([line.get("productName", "") for line in lines])
            quantity = sum([line.get("quantity", 1) for line in lines])
            status = order.get("status", "")
            rowbg = "#EFFAF3" if idx % 2 == 0 else "#F3EEFA"
            rowf = ctk.CTkFrame(self.orders_table, fg_color=rowbg)
            rowf.grid(row=idx+1, column=0, sticky="ew", pady=1, columnspan=5)
            ctk.CTkLabel(rowf, text=order_id, font=("Arial", 11), width=110).grid(row=0, column=0, padx=2)
            ctk.CTkLabel(rowf, text=customer, font=("Arial", 11), width=110).grid(row=0, column=1, padx=2)
            ctk.CTkLabel(rowf, text=products, font=("Arial", 11), width=120).grid(row=0, column=2, padx=2)
            ctk.CTkLabel(rowf, text=quantity, font=("Arial", 11), width=40).grid(row=0, column=3, padx=2)
            ctk.CTkLabel(rowf, text=status, font=("Arial", 11), width=80).grid(row=0, column=4, padx=2)