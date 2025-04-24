import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

PAZARYERI_LISTESI = [
    ("Trendyol", "trendyol"),
    ("N11", "n11"),
    ("Hepsiburada", "hepsiburada"),
    ("PTTAVM", "pttavm"),
    ("Pazarama", "pazarama"),
    ("Koçtaş", "koctas"),
]

MARKALAR = ["Seçiniz", "Samsung", "Apple", "Vestel", "Arçelik"]
KATEGORILER = ["Seçiniz", "Elektronik", "Ev & Yaşam", "Moda", "Oto", "Anne & Bebek"]
KDV_ORANLARI = ["%8", "%18", "%20"]
KARGO_FIRMALARI = ["Yurtiçi", "MNG", "Aras", "Sürat"]
URUN_DURUM = ["Yeni", "Kullanılmış"]
TESLIMAT_SURESI = [str(i) for i in range(1, 8)]
VITRINLER = ["Seçiniz", "Vitrin 1", "Vitrin 2"]
GARANTI_SURESI = ["6 Ay", "12 Ay", "24 Ay"]
STOK_TAKIP_TIPI = ["Manuel", "Otomatik"]
TESLIMAT_BOLGESI = ["Tüm Türkiye", "İstanbul", "Ege Bölgesi"]

class ProductUploadForm(ctk.CTkScrollableFrame):
    def __init__(self, master, trendyol_client=None):
        super().__init__(master, fg_color="white", corner_radius=10, width=1200, height=830)
        self.trendyol_client = trendyol_client
        self.selected_platforms = {k: ctk.BooleanVar() for t, k in PAZARYERI_LISTESI}
        self.urun_gorselleri = [None]*5
        self.urun_gorsel_paths = [None]*5
        self.gorsel_previews = []

        self.varyantlar = []

        self.build_form()

    def build_form(self):
        row = 0
        ctk.CTkLabel(self, text="Ürün Yükleme Paneli", font=("Arial", 26, "bold"), text_color="#222").grid(row=row, column=0, columnspan=6, pady=(20, 10), sticky="w")
        row += 1

        # Pazaryeri Seçimi
        ctk.CTkLabel(self, text="Pazaryeri Seçimi:", font=("Arial", 15, "bold")).grid(row=row, column=0, sticky="e", pady=6, padx=10)
        for i, (ad, anahtar) in enumerate(PAZARYERI_LISTESI):
            ctk.CTkCheckBox(self, text=ad, variable=self.selected_platforms[anahtar], command=self.platform_toggle).grid(row=row, column=1+i, sticky="w", padx=5)
        row += 1

        # Ortak Alanlar
        # Ürün Adı
        ctk.CTkLabel(self, text="Ürün Adı:", font=("Arial", 13)).grid(row=row, column=0, sticky="e", pady=6, padx=10)
        self.ent_urun_adi = ctk.CTkEntry(self, width=350)
        self.ent_urun_adi.grid(row=row, column=1, sticky="w", pady=6, padx=3, columnspan=2)
        row += 1

        # Açıklama
        ctk.CTkLabel(self, text="Açıklama:", font=("Arial", 13)).grid(row=row, column=0, sticky="ne", pady=6, padx=10)
        self.txt_aciklama = ctk.CTkTextbox(self, width=350, height=70)
        self.txt_aciklama.grid(row=row, column=1, sticky="w", pady=6, padx=3, columnspan=2)
        self.btn_aciklama_ai = ctk.CTkButton(self, text="Açıklamayı AI ile Öner", fg_color="#30A9E1", command=self.aciklama_ai_olustur)
        self.btn_aciklama_ai.grid(row=row, column=3, sticky="w", pady=6, padx=3)
        row += 1

        # Marka
        ctk.CTkLabel(self, text="Marka:", font=("Arial", 13)).grid(row=row, column=0, sticky="e", pady=6, padx=10)
        self.cmb_marka = ctk.CTkOptionMenu(self, values=MARKALAR)
        self.cmb_marka.set(MARKALAR[0])
        self.cmb_marka.grid(row=row, column=1, sticky="w", pady=6, padx=3)
        # Kategori
        ctk.CTkLabel(self, text="Kategori:", font=("Arial", 13)).grid(row=row, column=2, sticky="e", pady=6, padx=10)
        self.cmb_kategori = ctk.CTkOptionMenu(self, values=KATEGORILER)
        self.cmb_kategori.set(KATEGORILER[0])
        self.cmb_kategori.grid(row=row, column=3, sticky="w", pady=6, padx=3)
        row += 1

        # Fiyat
        ctk.CTkLabel(self, text="Fiyat (₺):", font=("Arial", 13)).grid(row=row, column=0, sticky="e", pady=6, padx=10)
        self.ent_fiyat = ctk.CTkEntry(self, width=120)
        self.ent_fiyat.grid(row=row, column=1, sticky="w", pady=6, padx=3)
        # KDV Oranı
        ctk.CTkLabel(self, text="KDV Oranı:", font=("Arial", 13)).grid(row=row, column=2, sticky="e", pady=6, padx=10)
        self.cmb_kdv = ctk.CTkOptionMenu(self, values=KDV_ORANLARI)
        self.cmb_kdv.set(KDV_ORANLARI[0])
        self.cmb_kdv.grid(row=row, column=3, sticky="w", pady=6, padx=3)
        row += 1

        # Stok Adedi
        ctk.CTkLabel(self, text="Stok Adedi:", font=("Arial", 13)).grid(row=row, column=0, sticky="e", pady=6, padx=10)
        self.ent_stok = ctk.CTkEntry(self, width=120)
        self.ent_stok.grid(row=row, column=1, sticky="w", pady=6, padx=3)
        # SKU
        ctk.CTkLabel(self, text="SKU:", font=("Arial", 13)).grid(row=row, column=2, sticky="e", pady=6, padx=10)
        self.ent_sku = ctk.CTkEntry(self, width=150)
        self.ent_sku.grid(row=row, column=3, sticky="w", pady=6, padx=3)
        # Barkod
        ctk.CTkLabel(self, text="Barkod:", font=("Arial", 13)).grid(row=row, column=4, sticky="e", pady=6, padx=10)
        self.ent_barkod = ctk.CTkEntry(self, width=150)
        self.ent_barkod.grid(row=row, column=5, sticky="w", pady=6, padx=3)
        row += 1

        # Desi
        ctk.CTkLabel(self, text="Desi:", font=("Arial", 13)).grid(row=row, column=0, sticky="e", pady=6, padx=10)
        self.ent_desi = ctk.CTkEntry(self, width=120)
        self.ent_desi.grid(row=row, column=1, sticky="w", pady=6, padx=3)
        row += 1

        # Kargo Firması
        ctk.CTkLabel(self, text="Kargo Firması:", font=("Arial", 13)).grid(row=row, column=0, sticky="e", pady=6, padx=10)
        self.cmb_kargo = ctk.CTkOptionMenu(self, values=KARGO_FIRMALARI)
        self.cmb_kargo.set(KARGO_FIRMALARI[0])
        self.cmb_kargo.grid(row=row, column=1, sticky="w", pady=6, padx=3)
        # Kargo Ücreti Kimden
        ctk.CTkLabel(self, text="Kargo Ücreti:", font=("Arial", 13)).grid(row=row, column=2, sticky="e", pady=6, padx=10)
        self.kargo_ucreti_var = ctk.StringVar(value="Satıcı")
        ctk.CTkRadioButton(self, text="Satıcı", variable=self.kargo_ucreti_var, value="Satıcı").grid(row=row, column=3, sticky="w", padx=3)
        ctk.CTkRadioButton(self, text="Alıcı", variable=self.kargo_ucreti_var, value="Alıcı").grid(row=row, column=4, sticky="w", padx=3)
        row += 1

        # Ürün Durumu
        ctk.CTkLabel(self, text="Ürün Durumu:", font=("Arial", 13)).grid(row=row, column=0, sticky="e", pady=6, padx=10)
        self.cmb_urun_durumu = ctk.CTkOptionMenu(self, values=URUN_DURUM)
        self.cmb_urun_durumu.set(URUN_DURUM[0])
        self.cmb_urun_durumu.grid(row=row, column=1, sticky="w", pady=6, padx=3)
        # Teslimat Süresi
        ctk.CTkLabel(self, text="Teslimat Süresi (gün):", font=("Arial", 13)).grid(row=row, column=2, sticky="e", pady=6, padx=10)
        self.cmb_teslimat = ctk.CTkOptionMenu(self, values=TESLIMAT_SURESI)
        self.cmb_teslimat.set(TESLIMAT_SURESI[0])
        self.cmb_teslimat.grid(row=row, column=3, sticky="w", pady=6, padx=3)
        row += 1

        # Etiketler
        ctk.CTkLabel(self, text="Ürün Etiketleri:", font=("Arial", 13)).grid(row=row, column=0, sticky="e", pady=6, padx=10)
        self.ent_etiketler = ctk.CTkEntry(self, width=350, placeholder_text="Virgül ile ayırınız (ör. hızlı,güvenli,yeni)")
        self.ent_etiketler.grid(row=row, column=1, sticky="w", pady=6, padx=3, columnspan=2)
        row += 1

        # Görsel Yükleme
        ctk.CTkLabel(self, text="Ürün Görselleri:", font=("Arial", 13)).grid(row=row, column=0, sticky="ne", pady=6, padx=10)
        gorsel_frame = ctk.CTkFrame(self, fg_color="white")
        gorsel_frame.grid(row=row, column=1, sticky="w", pady=6, padx=3, columnspan=5)
        for i in range(5):
            btn = ctk.CTkButton(gorsel_frame, text=f"Görsel {i+1} Yükle", command=lambda idx=i: self.gorsel_yukle(idx), width=120)
            btn.grid(row=0, column=i, padx=5)
            preview = ctk.CTkLabel(gorsel_frame, text="Önizleme", width=90, height=80, fg_color="#f3f3f3")
            preview.grid(row=1, column=i, padx=5, pady=3)
            self.gorsel_previews.append(preview)
        row += 1

        # Gelişmiş Ayarlar (Varyant Sistemi)
        self.var_gelismis = ctk.BooleanVar()
        self.chk_gelismis = ctk.CTkCheckBox(self, text="Gelişmiş Ayarları Göster (Varyant, AI, ...)", variable=self.var_gelismis, command=self.toggle_gelismis)
        self.chk_gelismis.grid(row=row, column=0, columnspan=3, sticky="w", padx=10, pady=6)
        row += 1
        self.gelismis_frame = ctk.CTkFrame(self, fg_color="#f2f6fa")
        self.gelismis_frame.grid(row=row, column=0, columnspan=6, sticky="we", padx=10, pady=6)
        self.gelismis_frame.grid_remove()  # Başlangıçta gizli

        # Varyant Sistemi başlık
        ctk.CTkLabel(self.gelismis_frame, text="Varyantlar (Renk/Beden):", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.btn_varyant_ekle = ctk.CTkButton(self.gelismis_frame, text="Varyant Ekle", command=self.varyant_ekle, width=120)
        self.btn_varyant_ekle.grid(row=0, column=1, padx=3, pady=8, sticky="w")
        self.varyant_satir = 1

        # --- Platforma Özel Alanlar
        row += 1
        self.platform_frames = {}

        # Trendyol
        self.platform_frames["trendyol"] = self.create_trendyol_alanlar(row)
        # Hepsiburada
        self.platform_frames["hepsiburada"] = self.create_hepsiburada_alanlar(row)
        # N11
        self.platform_frames["n11"] = self.create_n11_alanlar(row)
        # PTTAVM
        self.platform_frames["pttavm"] = self.create_pttavm_alanlar(row)
        # Pazarama
        self.platform_frames["pazarama"] = self.create_pazarama_alanlar(row)
        # Koçtaş
        self.platform_frames["koctas"] = self.create_koctas_alanlar(row)

        # İşlem Butonları
        btn_frame = ctk.CTkFrame(self, fg_color="white")
        btn_frame.grid(row=100, column=0, columnspan=6, pady=18)
        ctk.CTkButton(btn_frame, text="Ürünü Kaydet", fg_color="#24C38C", command=self.save_product, width=140).pack(side="left", padx=14)
        ctk.CTkButton(btn_frame, text="Önizleme Göster", fg_color="#30A9E1", command=self.preview_product, width=140).pack(side="left", padx=14)
        ctk.CTkButton(btn_frame, text="Formu Temizle", fg_color="#FF6B6B", command=self.clear_form, width=140).pack(side="left", padx=14)

    # ---- Platforma özel alanlar ----
    def create_trendyol_alanlar(self, base_row):
        frame = ctk.CTkFrame(self, fg_color="#FAFBFD")
        frame.grid(row=base_row+2, column=0, columnspan=6, sticky="we", padx=10, pady=6)
        frame.grid_remove()
        ctk.CTkLabel(frame, text="Tedarikçi Kodu:", font=("Arial", 13)).grid(row=0, column=0, sticky="e", pady=6, padx=10)
        self.ent_trendyol_tedarikci_kodu = ctk.CTkEntry(frame, width=150)
        self.ent_trendyol_tedarikci_kodu.grid(row=0, column=1, sticky="w", pady=6, padx=3)
        ctk.CTkLabel(frame, text="Garanti Süresi:", font=("Arial", 13)).grid(row=0, column=2, sticky="e", pady=6, padx=10)
        self.cmb_trendyol_garanti = ctk.CTkOptionMenu(frame, values=GARANTI_SURESI)
        self.cmb_trendyol_garanti.set(GARANTI_SURESI[0])
        self.cmb_trendyol_garanti.grid(row=0, column=3, sticky="w", pady=6, padx=3)
        return frame

    def create_hepsiburada_alanlar(self, base_row):
        frame = ctk.CTkFrame(self, fg_color="#FAFBFD")
        frame.grid(row=base_row+3, column=0, columnspan=6, sticky="we", padx=10, pady=6)
        frame.grid_remove()
        self.cb_hepsiburada_vitrin = ctk.BooleanVar()
        ctk.CTkCheckBox(frame, text="Ürün Vitrin Onayı", variable=self.cb_hepsiburada_vitrin).grid(row=0, column=0, pady=6, padx=10, sticky="w")
        return frame

    def create_n11_alanlar(self, base_row):
        frame = ctk.CTkFrame(self, fg_color="#FAFBFD")
        frame.grid(row=base_row+4, column=0, columnspan=6, sticky="we", padx=10, pady=6)
        frame.grid_remove()
        ctk.CTkLabel(frame, text="Vitrin Seçimi:", font=("Arial", 13)).grid(row=0, column=0, sticky="e", pady=6, padx=10)
        self.cmb_n11_vitrin = ctk.CTkOptionMenu(frame, values=VITRINLER)
        self.cmb_n11_vitrin.set(VITRINLER[0])
        self.cmb_n11_vitrin.grid(row=0, column=1, sticky="w", pady=6, padx=3)
        # Başlık karakter limiti kontrolü
        self.lbl_n11_baslik_limit = ctk.CTkLabel(frame, text="Başlık karakter limiti: 0/60", font=("Arial", 10), text_color="#FF6B6B")
        self.lbl_n11_baslik_limit.grid(row=0, column=2, sticky="w", padx=20)
        self.ent_urun_adi.bind("<KeyRelease>", self.n11_baslik_limit_kontrol)
        return frame

    def create_pttavm_alanlar(self, base_row):
        frame = ctk.CTkFrame(self, fg_color="#FAFBFD")
        frame.grid(row=base_row+5, column=0, columnspan=6, sticky="we", padx=10, pady=6)
        frame.grid_remove()
        ctk.CTkLabel(frame, text="Gümrük Kodu:", font=("Arial", 13)).grid(row=0, column=0, sticky="e", pady=6, padx=10)
        self.ent_pttavm_gumruk_kodu = ctk.CTkEntry(frame, width=150)
        self.ent_pttavm_gumruk_kodu.grid(row=0, column=1, sticky="w", pady=6, padx=3)
        self.cb_pttavm_kdv_dahil = ctk.BooleanVar()
        ctk.CTkCheckBox(frame, text="KDV Dahil mi?", variable=self.cb_pttavm_kdv_dahil).grid(row=0, column=2, pady=6, padx=10, sticky="w")
        return frame

    def create_pazarama_alanlar(self, base_row):
        frame = ctk.CTkFrame(self, fg_color="#FAFBFD")
        frame.grid(row=base_row+6, column=0, columnspan=6, sticky="we", padx=10, pady=6)
        frame.grid_remove()
        ctk.CTkLabel(frame, text="Kampanya Adı:", font=("Arial", 13)).grid(row=0, column=0, sticky="e", pady=6, padx=10)
        self.ent_pazarama_kampanya = ctk.CTkEntry(frame, width=150)
        self.ent_pazarama_kampanya.grid(row=0, column=1, sticky="w", pady=6, padx=3)
        ctk.CTkLabel(frame, text="Stok Takip Tipi:", font=("Arial", 13)).grid(row=0, column=2, sticky="e", pady=6, padx=10)
        self.cmb_pazarama_stok_takip = ctk.CTkOptionMenu(frame, values=STOK_TAKIP_TIPI)
        self.cmb_pazarama_stok_takip.set(STOK_TAKIP_TIPI[0])
        self.cmb_pazarama_stok_takip.grid(row=0, column=3, sticky="w", pady=6, padx=3)
        return frame

    def create_koctas_alanlar(self, base_row):
        frame = ctk.CTkFrame(self, fg_color="#FAFBFD")
        frame.grid(row=base_row+7, column=0, columnspan=6, sticky="we", padx=10, pady=6)
        frame.grid_remove()
        ctk.CTkLabel(frame, text="Sertifika Dosyası:", font=("Arial", 13)).grid(row=0, column=0, sticky="e", pady=6, padx=10)
        self.ent_koctas_sertifika = ctk.CTkEntry(frame, width=180)
        self.ent_koctas_sertifika.grid(row=0, column=1, sticky="w", pady=6, padx=3)
        btn = ctk.CTkButton(frame, text="Yükle", command=self.koctas_sertifika_yukle, width=80)
        btn.grid(row=0, column=2, padx=5)
        ctk.CTkLabel(frame, text="Teslimat Bölgesi:", font=("Arial", 13)).grid(row=0, column=3, sticky="e", pady=6, padx=10)
        self.cmb_koctas_bolge = ctk.CTkOptionMenu(frame, values=TESLIMAT_BOLGESI)
        self.cmb_koctas_bolge.set(TESLIMAT_BOLGESI[0])
        self.cmb_koctas_bolge.grid(row=0, column=4, sticky="w", pady=6, padx=3)
        return frame

    # ---- Event/Callback fonksiyonları ----
    def platform_toggle(self):
        for anahtar, frame in self.platform_frames.items():
            if self.selected_platforms[anahtar].get():
                frame.grid()
            else:
                frame.grid_remove()

    def gorsel_yukle(self, idx):
        file_path = filedialog.askopenfilename(filetypes=[("Resim Dosyası", "*.png;*.jpg;*.jpeg;*.webp;*.bmp")])
        if file_path:
            self.urun_gorsel_paths[idx] = file_path
            img = Image.open(file_path)
            img.thumbnail((80, 80))
            img = ImageTk.PhotoImage(img)
            self.urun_gorselleri[idx] = img
            self.gorsel_previews[idx].configure(image=img, text="")
            self.gorsel_previews[idx].image = img

    def koctas_sertifika_yukle(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Dosyası", "*.pdf"), ("Tüm Dosyalar", "*.*")])
        if file_path:
            self.ent_koctas_sertifika.delete(0, "end")
            self.ent_koctas_sertifika.insert(0, file_path)

    def n11_baslik_limit_kontrol(self, event=None):
        metin = self.ent_urun_adi.get()
        self.lbl_n11_baslik_limit.configure(text=f"Başlık karakter limiti: {len(metin)}/60")
        if len(metin) > 60:
            self.lbl_n11_baslik_limit.configure(text_color="#FF0000")
        else:
            self.lbl_n11_baslik_limit.configure(text_color="#FF6B6B")

    def toggle_gelismis(self):
        if self.var_gelismis.get():
            self.gelismis_frame.grid()
        else:
            self.gelismis_frame.grid_remove()

    def varyant_ekle(self):
        satir = self.varyant_satir
        renk = ctk.CTkEntry(self.gelismis_frame, width=110, placeholder_text="Renk")
        renk.grid(row=satir, column=0, padx=10, pady=3)
        beden = ctk.CTkEntry(self.gelismis_frame, width=110, placeholder_text="Beden")
        beden.grid(row=satir, column=1, padx=10, pady=3)
        stok = ctk.CTkEntry(self.gelismis_frame, width=80, placeholder_text="Stok")
        stok.grid(row=satir, column=2, padx=10, pady=3)
        self.varyantlar.append((renk, beden, stok))
        self.varyant_satir += 1

    def aciklama_ai_olustur(self):
        # OpenAI API ile açıklama önerisi entegrasyonu burada yapılabilir
        messagebox.showinfo("AI Açıklama", "AI destekli açıklama önerisi burada gösterilecek (OpenAI API ile bağlayabilirsin).")

    def save_product(self):
        # Tüm alanlardan verileri çek, platform kontrollerini ve validasyonları uygula
        messagebox.showinfo("Kayıt", "Ürün kaydedildi (demo).")

    def preview_product(self):
        messagebox.showinfo("Önizleme", "Ürün önizlemesi (demo).")

    def clear_form(self):
        self.ent_urun_adi.delete(0, "end")
        self.txt_aciklama.delete("1.0", "end")
        self.cmb_marka.set(MARKALAR[0])
        self.cmb_kategori.set(KATEGORILER[0])
        self.ent_fiyat.delete(0, "end")
        self.cmb_kdv.set(KDV_ORANLARI[0])
        self.ent_stok.delete(0, "end")
        self.ent_sku.delete(0, "end")
        self.ent_barkod.delete(0, "end")
        self.ent_desi.delete(0, "end")
        self.cmb_kargo.set(KARGO_FIRMALARI[0])
        self.kargo_ucreti_var.set("Satıcı")
        self.cmb_urun_durumu.set(URUN_DURUM[0])
        self.cmb_teslimat.set(TESLIMAT_SURESI[0])
        self.ent_etiketler.delete(0, "end")
        # Görseller
        for i in range(5):
            self.urun_gorsel_paths[i] = None
            self.urun_gorselleri[i] = None
            self.gorsel_previews[i].configure(image=None, text="Önizleme")
        # Gelişmiş ayarları temizle
        for renk, beden, stok in self.varyantlar:
            renk.destroy()
            beden.destroy()
            stok.destroy()
        self.varyantlar.clear()
        self.varyant_satir = 1
        # Platform özel alanları temizle
        self.ent_trendyol_tedarikci_kodu.delete(0, "end")
        self.cmb_trendyol_garanti.set(GARANTI_SURESI[0])
        self.cb_hepsiburada_vitrin.set(False)
        self.cmb_n11_vitrin.set(VITRINLER[0])
        self.ent_pttavm_gumruk_kodu.delete(0, "end")
        self.cb_pttavm_kdv_dahil.set(False)
        self.ent_pazarama_kampanya.delete(0, "end")
        self.cmb_pazarama_stok_takip.set(STOK_TAKIP_TIPI[0])
        self.ent_koctas_sertifika.delete(0, "end")
        self.cmb_koctas_bolge.set(TESLIMAT_BOLGESI[0])
        # Platform seçimlerini sıfırla
        for v in self.selected_platforms.values():
            v.set(False)
        self.platform_toggle()
        self.var_gelismis.set(False)
        self.toggle_gelismis()