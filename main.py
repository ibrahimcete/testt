import customtkinter as ctk
from api_clients import TrendyolClient
from login import LoginFrame
from dashboard import Dashboard
from product_upload_form import ProductUploadForm
from product_list import ProductList
from order_management import OrderManagement
from order_detail import OrderDetail
from reports import Reports
from notifications import Notifications
from user_management import UserManagement

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
SUPPLIER_ID = "your_supplier_id"

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pazaryeri Entegrasyon Paneli")
        self.geometry("1440x900")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.resizable(False, False)
        self.trendyol_client = TrendyolClient(API_KEY, API_SECRET, SUPPLIER_ID)
        self.logged_in_user = None

        self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color="#1E293B")
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        self.sidebar_frame.grid_rowconfigure(12, weight=1)

        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.show_login()

    def show_login(self):
        self.clear_main_frame()
        login_frame = LoginFrame(self.main_frame, self.login_success)
        login_frame.pack(expand=True)

    def login_success(self, user):
        self.logged_in_user = user
        self.create_sidebar()
        self.show_dashboard()

    def create_sidebar(self):
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.sidebar_frame, text="Panel Menüsü", font=("Roboto", 24, "bold"), text_color="white").grid(row=0, column=0, padx=20, pady=(20, 10))
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Ürün Yükleme", self.show_product_upload),
            ("Ürün Listesi", self.show_product_list),
            ("Sipariş Yönetimi", self.show_order_management),
            ("Sipariş Detayları", self.show_order_detail),
            ("Raporlar", self.show_reports),
            ("Bildirimler", self.show_notifications),
            ("Kullanıcı Yönetimi", self.show_users)
        ]
        row = 1
        for (text, command) in nav_buttons:
            ctk.CTkButton(self.sidebar_frame, text=text, font=("Roboto", 16), fg_color="#00C49F", hover_color="#38BDF8", command=command).grid(row=row, column=0, padx=20, pady=5, sticky="ew")
            row += 1
        ctk.CTkButton(self.sidebar_frame, text="Çıkış", font=("Roboto", 16), fg_color="red", hover_color="#FF6B6B", command=self.logout).grid(row=row, column=0, padx=20, pady=20, sticky="ew")

    def show_dashboard(self):
        self.clear_main_frame()
        Dashboard(self.main_frame, self.trendyol_client).pack(fill="both", expand=True)

    def show_product_upload(self):
        self.clear_main_frame()
        ProductUploadForm(self.main_frame, self.trendyol_client).pack(fill="both", expand=True)

    def show_product_list(self):
        self.clear_main_frame()
        ProductList(self.main_frame, self.trendyol_client).pack(fill="both", expand=True)

    def show_order_management(self):
        self.clear_main_frame()
        OrderManagement(self.main_frame, self.trendyol_client).pack(fill="both", expand=True)

    def show_order_detail(self):
        self.clear_main_frame()
        OrderDetail(self.main_frame, self.trendyol_client).pack(fill="both", expand=True)

    def show_reports(self):
        self.clear_main_frame()
        Reports(self.main_frame, self.trendyol_client).pack(fill="both", expand=True)

    def show_notifications(self):
        self.clear_main_frame()
        Notifications(self.main_frame).pack(fill="both", expand=True)

    def show_users(self):
        self.clear_main_frame()
        UserManagement(self.main_frame).pack(fill="both", expand=True)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def logout(self):
        self.logged_in_user = None
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()
        self.show_login()

    def on_close(self):
        self.destroy()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()