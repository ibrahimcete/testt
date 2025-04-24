import customtkinter as ctk
from tkinter import messagebox, Toplevel
from datetime import datetime
from tkcalendar import DateEntry

PAZARYERI_LISTESI = [
    ("Trendyol", "trendyol"),
    ("Hepsiburada", "hepsiburada"),
    ("N11", "n11"),
    ("PTTAVM", "pttavm"),
    ("Pazarama", "pazarama"),
    ("Koçtaş", "koctas"),
]

SIPARIS_DURUMLARI = ["Bekliyor", "Kargolandı", "İptal Edildi", "İade Edildi"]
KARGO_FIRMALARI = ["Yurtiçi", "MNG", "Aras", "Sürat"]

class OrderManagement(ctk.CTkFrame):
    def __init__(self, master, trendyol_client):
        super().__init__(master)
        self.trendyol_client = trendyol_client
        self.configure(fg_color="white")
        self.selected_platforms = {k: ctk.BooleanVar(value=True) for t, k in PAZARYERI_LISTESI}
        self.selected_status = ctk.StringVar(value=SIPARIS_DURUMLARI[0])
        self.search_text = ctk.StringVar()
        self.start_date = ctk.StringVar(value=datetime.now().strftime("%Y-%m-01"))
        self.end_date = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.api_logs = []
        self.advanced_visible = ctk.BooleanVar(value=False)
        self.auto_cargo_mode = ctk.BooleanVar(value=False)
        self.selected_order = None
        self.orders = []
        self.filter_panel()
        self.order_list_panel()
        self.bottom_buttons()
        self.advanced_panel()

    def filter_panel(self):
        # Başlık ve açıklama
        ctk.CTkLabel(self, text="Sipariş Yönetimi", font=("Arial", 28, "bold"), text_color="#1E293B").grid(row=0, column=0, columnspan=10, sticky="w", padx=22, pady=(16,2))
        ctk.CTkLabel(self, text="Tüm pazaryerlerinden gelen siparişleri filtreleyebilir, görüntüleyebilir ve kargolayabilirsiniz.",
                     font=("Arial", 14), text_color="#405060").grid(row=1, column=0, columnspan=10, sticky="w", padx=22, pady=(2,12))
        filter_frame = ctk.CTkFrame(self, fg_color="#F8FAFC", corner_radius=10)
        filter_frame.grid(row=2, column=0, columnspan=10, sticky="we", padx=14, pady=(0, 8))
        # Pazaryeri seçim
        ctk.CTkLabel(filter_frame, text="Pazaryeri:", font=("Arial", 13)).grid(row=0, column=0, padx=8, pady=8, sticky="e")
        for i, (ad, anahtar) in enumerate(PAZARYERI_LISTESI):
            ctk.CTkCheckBox(filter_frame, text=ad, variable=self.selected_platforms[anahtar]).grid(row=0, column=1+i, padx=3, sticky="w")
        # Sipariş durumu
        ctk.CTkLabel(filter_frame, text="Durum:", font=("Arial", 13)).grid(row=0, column=8, padx=8, pady=8, sticky="e")
        ctk.CTkOptionMenu(filter_frame, variable=self.selected_status, values=SIPARIS_DURUMLARI, width=110).grid(row=0, column=9, padx=5, sticky="w")
        # Arama
        ctk.CTkLabel(filter_frame, text="Ara:", font=("Arial", 13)).grid(row=1, column=0, padx=8, pady=8, sticky="e")
        ctk.CTkEntry(filter_frame, textvariable=self.search_text, width=180, placeholder_text="Sipariş No / Müşteri Adı").grid(row=1, column=1, columnspan=2, padx=5, sticky="w")
        # Tarih aralığı
        ctk.CTkLabel(filter_frame, text="Başlangıç:", font=("Arial", 13)).grid(row=1, column=3, padx=5, sticky="e")
        self.start_date_picker = DateEntry(filter_frame, textvariable=self.start_date, date_pattern="yyyy-mm-dd", width=12, font=("Arial", 11))
        self.start_date_picker.grid(row=1, column=4, padx=2, sticky="w")
        ctk.CTkLabel(filter_frame, text="Bitiş:", font=("Arial", 13)).grid(row=1, column=5, padx=5, sticky="e")
        self.end_date_picker = DateEntry(filter_frame, textvariable=self.end_date, date_pattern="yyyy-mm-dd", width=12, font=("Arial", 11))
        self.end_date_picker.grid(row=1, column=6, padx=2, sticky="w")
        # Siparişleri Getir Butonu
        ctk.CTkButton(filter_frame, text="Siparişleri Getir", fg_color="#24C38C", command=self.get_orders, width=140).grid(row=1, column=7, padx=18, pady=4, sticky="w")
        # Gelişmiş Panel Aç/Kapa
        ctk.CTkButton(filter_frame, text="Gelişmiş ▼", fg_color="#30A9E1", width=90, command=self.toggle_advanced).grid(row=1, column=9, padx=8, pady=4, sticky="e")

    def order_list_panel(self):
        # Tablo başlıkları
        self.table_frame = ctk.CTkFrame(self, fg_color="white")
        self.table_frame.grid(row=3, column=0, columnspan=10, padx=14, pady=(0,8), sticky="nsew")
        col_titles = ["Sipariş No", "Müşteri Adı", "Ürün Adı", "Adet", "Birim Fiyat", "Toplam Tutar",
                      "Sipariş Durumu", "Pazaryeri", "Kargo Takip No", "İşlem"]
        for i, title in enumerate(col_titles):
            ctk.CTkLabel(self.table_frame, text=title, font=("Arial", 12, "bold"), text_color="#222").grid(row=0, column=i, padx=4, pady=(4,2))
        # Scrollable sipariş listesi
        self.order_scroll = ctk.CTkScrollableFrame(self.table_frame, fg_color="#FAFBFD", height=350, corner_radius=5)
        self.order_scroll.grid(row=1, column=0, columnspan=10, sticky="nsew", padx=2, pady=2)
        self.table_frame.grid_rowconfigure(1, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.refresh_order_list([])

    def refresh_order_list(self, orders):
        for widget in self.order_scroll.winfo_children():
            widget.destroy()
        self.orders = orders
        for idx, order in enumerate(orders):
            bg = "#F3F9F3" if idx % 2 == 0 else "#F8F8FF"
            row_frame = ctk.CTkFrame(self.order_scroll, fg_color=bg)
            row_frame.grid(row=idx, column=0, sticky="ew", padx=0, pady=0)
            # Sipariş bilgileri
            vals = [
                order.get("order_no", ""),
                order.get("customer_name", ""),
                order.get("product_name", ""),
                str(order.get("quantity", "")),
                f"{order.get('unit_price', '')}₺",
                f"{order.get('total', '')}₺",
                order.get("status", ""),
                order.get("marketplace", ""),
                order.get("cargo_track_no", ""),
            ]
            for i, v in enumerate(vals):
                l = ctk.CTkLabel(row_frame, text=v, font=("Arial", 11), width=90, anchor="w")
                l.grid(row=0, column=i, padx=3, pady=2, sticky="w")
            # İşlemler
            btn_detay = ctk.CTkButton(row_frame, text="Detay", fg_color="#30A9E1", width=54, command=lambda o=order: self.show_order_detail(o))
            btn_detay.grid(row=0, column=9, padx=(2,2), pady=2, sticky="w")
            btn_kargola = ctk.CTkButton(row_frame, text="Kargola", fg_color="#24C38C", width=54, command=lambda o=order: self.kargola_order(o))
            btn_kargola.grid(row=0, column=10, padx=(2,2), pady=2, sticky="w")
            btn_iptal = ctk.CTkButton(row_frame, text="İptal", fg_color="#FF6B6B", width=54, command=lambda o=order: self.iptal_order(o))
            btn_iptal.grid(row=0, column=11, padx=(2,2), pady=2, sticky="w")
            row_frame.bind("<Button-1>", lambda e, o=order: self.select_order(o))
            for child in row_frame.winfo_children():
                child.bind("<Button-1>", lambda e, o=order: self.select_order(o))

    def select_order(self, order):
        self.selected_order = order

    def show_order_detail(self, order):
        win = Toplevel(self)
        win.title("Sipariş Detay")
        win.geometry("420x450")
        ctk.CTkLabel(win, text="Sipariş Detayı", font=("Arial", 18, "bold")).pack(pady=10)
        # Ürün bilgileri
        ctk.CTkLabel(win, text=f"Ürün: {order.get('product_name', '')}", font=("Arial", 13)).pack(anchor="w", padx=20, pady=4)
        ctk.CTkLabel(win, text=f"Adet: {order.get('quantity', '')}", font=("Arial", 13)).pack(anchor="w", padx=20, pady=4)
        ctk.CTkLabel(win, text=f"Fiyat: {order.get('unit_price', '')}₺", font=("Arial", 13)).pack(anchor="w", padx=20, pady=4)
        # Müşteri adres/bilgi
        ctk.CTkLabel(win, text=f"Adres: {order.get('customer_address', '')}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=4)
        ctk.CTkLabel(win, text=f"Telefon: {order.get('customer_phone', '')}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(win, text=f"E-posta: {order.get('customer_email', '')}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=2)
        # Kargo firması
        ctk.CTkLabel(win, text="Kargo Firması:", font=("Arial", 13)).pack(anchor="w", padx=20, pady=(12, 2))
        kargo_var = ctk.StringVar(value=order.get("cargo_company", KARGO_FIRMALARI[0]))
        cmb_kargo = ctk.CTkOptionMenu(win, variable=kargo_var, values=KARGO_FIRMALARI)
        cmb_kargo.pack(anchor="w", padx=22, pady=2)
        # Kargo takip no
        ctk.CTkLabel(win, text="Kargo Takip No:", font=("Arial", 13)).pack(anchor="w", padx=20, pady=(10,2))
        ent_kargo_no = ctk.CTkEntry(win, width=180)
        ent_kargo_no.insert(0, order.get("cargo_track_no", ""))
        ent_kargo_no.pack(anchor="w", padx=22, pady=2)
        # Not
        ctk.CTkLabel(win, text="Sipariş Notu:", font=("Arial", 13)).pack(anchor="w", padx=20, pady=(10,2))
        txt_not = ctk.CTkTextbox(win, width=320, height=40)
        txt_not.insert("1.0", order.get("note", ""))
        txt_not.pack(anchor="w", padx=22, pady=2)
        # Kaydet Butonu
        ctk.CTkButton(win, text="Kaydet", fg_color="#24C38C", width=140,
                      command=lambda: self.save_order_detail(order, kargo_var.get(), ent_kargo_no.get(), txt_not.get("1.0", "end"), win)).pack(pady=18)

    def save_order_detail(self, order, kargo_firma, kargo_no, notu, win):
        order["cargo_company"] = kargo_firma
        order["cargo_track_no"] = kargo_no
        order["note"] = notu.strip()
        self.api_logs.append(f"{datetime.now()}: Sipariş güncellendi ({order.get('order_no')})")
        messagebox.showinfo("Kaydedildi", "Sipariş detayları kaydedildi.")
        win.destroy()
        self.refresh_order_list(self.orders)

    def kargola_order(self, order):
        messagebox.showinfo("Kargo", f"Sipariş {order.get('order_no')} kargolandı (Demo).")
        self.api_logs.append(f"{datetime.now()}: Kargo işlemi gönderildi ({order.get('order_no')})")

    def iptal_order(self, order):
        messagebox.showwarning("İptal", f"Sipariş {order.get('order_no')} iptal edildi (Demo).")
        self.api_logs.append(f"{datetime.now()}: Sipariş iptal edildi ({order.get('order_no')})")

    def get_orders(self):
        # Demo sipariş verisi
        orders = [
            {
                "order_no": "TY-12345",
                "customer_name": "Ahmet Yılmaz",
                "product_name": "Bluetooth Kulaklık",
                "quantity": 2,
                "unit_price": 600,
                "total": 1200,
                "status": self.selected_status.get(),
                "marketplace": "Trendyol",
                "cargo_track_no": "YK12345678",
                "customer_address": "İstanbul, Türkiye",
                "customer_phone": "0555 123 4567",
                "customer_email": "ahmet@example.com",
                "cargo_company": "Yurtiçi",
                "note": ""
            },
            {
                "order_no": "N11-555",
                "customer_name": "Mehmet Kaya",
                "product_name": "Laptop",
                "quantity": 1,
                "unit_price": 12000,
                "total": 12000,
                "status": self.selected_status.get(),
                "marketplace": "N11",
                "cargo_track_no": "",
                "customer_address": "Ankara, Türkiye",
                "customer_phone": "0531 111 2222",
                "customer_email": "mehmet.kaya@example.com",
                "cargo_company": "MNG",
                "note": ""
            },
        ]
        self.refresh_order_list(orders)
        self.api_logs.append(f"{datetime.now()}: {len(orders)} adet sipariş listelendi")

    def bottom_buttons(self):
        bottom = ctk.CTkFrame(self, fg_color="#FFFFFF")
        bottom.grid(row=99, column=0, columnspan=10, sticky="sew", pady=(10, 0), padx=12)
        ctk.CTkButton(bottom, text="Seçili Siparişi Kargola", fg_color="#24C38C", command=self.kargola_selected, width=160).pack(side="left", padx=8, pady=10)
        ctk.CTkButton(bottom, text="Seçili Siparişi Güncelle", fg_color="#30A9E1", command=self.guncelle_selected, width=160).pack(side="left", padx=8)
        ctk.CTkButton(bottom, text="Seçili Siparişi İptal Et", fg_color="#FF6B6B", command=self.iptal_selected, width=160).pack(side="left", padx=8)
        ctk.CTkButton(bottom, text="Tüm Siparişleri Yenile", fg_color="#A259FF", command=self.get_orders, width=160).pack(side="left", padx=8)
        ctk.CTkButton(bottom, text="Hatalı Siparişleri Göster", fg_color="#FFE066", text_color="#B58900", command=self.show_logs, width=180).pack(side="right", padx=8)

    def kargola_selected(self):
        if self.selected_order:
            self.kargola_order(self.selected_order)
        else:
            messagebox.showwarning("Uyarı", "Lütfen önce bir sipariş seçiniz.")

    def guncelle_selected(self):
        if self.selected_order:
            self.show_order_detail(self.selected_order)
        else:
            messagebox.showwarning("Uyarı", "Lütfen önce bir sipariş seçiniz.")

    def iptal_selected(self):
        if self.selected_order:
            self.iptal_order(self.selected_order)
        else:
            messagebox.showwarning("Uyarı", "Lütfen önce bir sipariş seçiniz.")

    def show_logs(self):
        win = Toplevel(self)
        win.title("API Logları - Hatalı Siparişler")
        win.geometry("500x400")
        log_box = ctk.CTkTextbox(win, width=460, height=340)
        log_box.pack(padx=16, pady=16)
        logs = "\n".join(self.api_logs)
        log_box.insert("1.0", logs if logs else "Henüz hata kaydı yok.")

    def advanced_panel(self):
        self.adv_frame = ctk.CTkFrame(self, fg_color="#F8FAFC", corner_radius=10)
        self.adv_frame.grid(row=98, column=0, columnspan=10, sticky="we", padx=14, pady=(0, 2))
        self.adv_frame.grid_remove()
        # Otomatik Kargo Modu
        ctk.CTkCheckBox(self.adv_frame, text="Otomatik Kargo Modu", variable=self.auto_cargo_mode).grid(row=0, column=0, padx=12, pady=8, sticky="w")
        # API Logları
        ctk.CTkButton(self.adv_frame, text="API Loglarını Göster", fg_color="#30A9E1", command=self.show_logs, width=170).grid(row=0, column=1, padx=18, sticky="w")
        # Yeni Sipariş Bildirimi (Demo popup)
        ctk.CTkButton(self.adv_frame, text="Yeni Sipariş Bildirimi Göster", fg_color="#24C38C", command=self.yeni_siparis_bildirimi, width=200).grid(row=0, column=2, padx=18, sticky="w")

    def toggle_advanced(self):
        if self.advanced_visible.get():
            self.adv_frame.grid_remove()
            self.advanced_visible.set(False)
        else:
            self.adv_frame.grid()
            self.advanced_visible.set(True)

    def yeni_siparis_bildirimi(self):
        win = Toplevel(self)
        win.title("Yeni Sipariş Bildirimi")
        win.geometry("340x130")
        ctk.CTkLabel(win, text="Yeni Sipariş Geldi!", font=("Arial", 16, "bold"), text_color="#24C38C").pack(pady=18)
        ctk.CTkLabel(win, text="Sipariş No: TY-99999\nMüşteri: Ali Veli\nÜrün: Akıllı Saat", font=("Arial", 13)).pack(pady=6)
        ctk.CTkButton(win, text="Kapat", command=win.destroy, fg_color="#A259FF", width=60).pack(pady=8)