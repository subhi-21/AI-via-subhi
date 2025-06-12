import customtkinter as ctk
from tkinter import messagebox
import json
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# إعداد الواجهة
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ORANGE = "#FFA500"
WHITE = "#FFFFFF"
ORDERS_FILE = "orders.json"

def load_orders():
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "w") as f:
            json.dump({}, f)
    with open(ORDERS_FILE, "r") as f:
        return json.load(f)

def save_orders(data):
    with open(ORDERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):
        return False
    return True

orders_data = load_orders()
user_data = {}

app = ctk.CTk()
app.geometry("600x600")
app.title("Techno Event")

translations = {
    "en": {
        "login_title": "Login to Techno Event",
        "email_placeholder": "Email",
        "password_placeholder": "Password (8+ chars, with numbers)",
        "login_btn": "Login",
        "input_error": "Please enter email and password.",
        "email_invalid": "Enter valid email.",
        "password_invalid": "Password min 8 chars, include numbers.",
        "login_failed": "Wrong password.",
        "welcome": "Welcome, {}",
        "new_request": "New Event Request",
        "view_orders": "View My Orders",
        "logout": "Logout",
        "event_form_title": "Event Request Form",
        "select_event_type": "Select Event Type:",
        "screen_type": "Screen Type:",
        "screen_size": "Screen Size (m²)",
        "additional_requests": "Additional Requests",
        "submit_order": "Submit Order",
        "missing_size": "Enter screen size.",
        "invalid_size": "Screen size must be a number.",
        "confirm_request": "Confirm your request?",
        "submitted_msg": "Thank you. We'll reply within 24h.",
        "my_orders": "My Orders",
        "no_orders": "No orders found.",
        "back_to_menu": "Back to Menu",
        "language": "Language:",
        "festival": "Festival",
        "wedding": "Wedding",
        "conference": "Conference",
        "other": "Other",
        "indoor": "Indoor",
        "outdoor": "Outdoor",
    },
    "ar": {
        "login_title": "تسجيل الدخول إلى تكنو إيفنت",
        "email_placeholder": "البريد الإلكتروني",
        "password_placeholder": "كلمة السر (8 أحرف على الأقل وبها أرقام)",
        "login_btn": "تسجيل الدخول",
        "input_error": "يرجى إدخال البريد الإلكتروني وكلمة السر.",
        "email_invalid": "يرجى إدخال بريد إلكتروني صحيح.",
        "password_invalid": "كلمة السر يجب أن تكون 8 أحرف على الأقل وتحتوي على أرقام.",
        "login_failed": "كلمة السر غير صحيحة.",
        "welcome": "مرحباً، {}",
        "new_request": "طلب فعالية جديدة",
        "view_orders": "عرض طلباتي",
        "logout": "تسجيل خروج",
        "event_form_title": "نموذج طلب الفعالية",
        "select_event_type": "اختر نوع الفعالية:",
        "screen_type": "نوع الشاشة:",
        "screen_size": "حجم الشاشة (م²)",
        "additional_requests": "طلبات إضافية",
        "submit_order": "إرسال الطلب",
        "missing_size": "يرجى إدخال حجم الشاشة.",
        "invalid_size": "حجم الشاشة يجب أن يكون رقم.",
        "confirm_request": "هل أنت متأكد من طلبك؟",
        "submitted_msg": "شكراً لتعاملك معنا.\nسوف يتم الرد خلال 24 ساعة.",
        "my_orders": "طلباتي",
        "no_orders": "لا توجد طلبات.",
        "back_to_menu": "العودة للقائمة",
        "language": "اللغة:",
        "festival": "فيستيفال",
        "wedding": "عرس",
        "conference": "مؤتمر",
        "other": "أخرى",
        "indoor": "داخلية",
        "outdoor": "خارجية",
    },
    "tr": {
        "login_title": "Techno Event Giriş",
        "email_placeholder": "E-posta",
        "password_placeholder": "Şifre (8+ karakter, rakam dahil)",
        "login_btn": "Giriş Yap",
        "input_error": "Lütfen e-posta ve şifre girin.",
        "email_invalid": "Geçerli e-posta girin.",
        "password_invalid": "Şifre en az 8 karakter ve rakam içermelidir.",
        "login_failed": "Şifre yanlış.",
        "welcome": "Hoşgeldiniz, {}",
        "new_request": "Yeni Etkinlik Talebi",
        "view_orders": "Siparişlerim",
        "logout": "Çıkış Yap",
        "event_form_title": "Etkinlik Talep Formu",
        "select_event_type": "Etkinlik Türünü Seçin:",
        "screen_type": "Ekran Tipi:",
        "screen_size": "Ekran Boyutu (m²)",
        "additional_requests": "Ek Talepler",
        "submit_order": "Siparişi Gönder",
        "missing_size": "Ekran boyutunu girin.",
        "invalid_size": "Ekran boyutu sayı olmalı.",
        "confirm_request": "Talebinizi onaylıyor musunuz?",
        "submitted_msg": "Teşekkürler. 24 saat içinde dönüş yapılacak.",
        "my_orders": "Siparişlerim",
        "no_orders": "Sipariş yok.",
        "back_to_menu": "Menüye Dön",
        "language": "Dil:",
        "festival": "Festival",
        "wedding": "Düğün",
        "conference": "Konferans",
        "other": "Diğer",
        "indoor": "İç Mekan",
        "outdoor": "Dış Mekan",
    }
}

current_lang = "en"
def t(key):
    return translations[current_lang].get(key, key)

def send_email(subject, body):
    # **عدل بيانات الإيميل هنا**
    sender_email = "yourcompanyemail@example.com"
    sender_password = "your_email_app_password"
    receiver_email = "orders@yourcompany.com"

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent")
    except Exception as e:
        print("Email sending failed:", e)

def clear_frame():
    for widget in app.winfo_children():
        widget.destroy()

def show_login_frame():
    global current_lang
    clear_frame()

    ctk.CTkLabel(app, text=t("login_title"), font=("Arial", 24, "bold"), text_color=ORANGE).pack(pady=20)

    lang_var = ctk.StringVar(value=current_lang)
    def on_lang_change(choice):
        global current_lang
        current_lang = choice
        show_login_frame()
    ctk.CTkLabel(app, text=t("language"), text_color=WHITE).pack()
    ctk.CTkOptionMenu(app, values=["en", "ar", "tr"], variable=lang_var, command=on_lang_change).pack(pady=5)

    email_entry = ctk.CTkEntry(app, placeholder_text=t("email_placeholder"))
    email_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(app, placeholder_text=t("password_placeholder"), show="*")
    password_entry.pack(pady=10)

    def login_action():
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Input Error", t("input_error"))
            return
        if not is_valid_email(email):
            messagebox.showwarning("Input Error", t("email_invalid"))
            return
        if not is_valid_password(password):
            messagebox.showwarning("Input Error", t("password_invalid"))
            return

        user_data["email"] = email
        user_data["password"] = password

        if email not in orders_data:
            orders_data[email] = {"password": password, "orders": []}
            save_orders(orders_data)
        else:
            if orders_data[email]["password"] != password:
                messagebox.showerror("Login Failed", t("login_failed"))
                return

        show_main_menu()

    ctk.CTkButton(app, text=t("login_btn"), fg_color=ORANGE, text_color=WHITE, command=login_action).pack(pady=20)

def show_main_menu():
    clear_frame()

    ctk.CTkLabel(app, text=t("welcome").format(user_data["email"]), font=("Arial", 20, "bold"), text_color=ORANGE).pack(pady=15)

    ctk.CTkButton(app, text=t("new_request"), fg_color=ORANGE, command=show_form_frame).pack(pady=10)
    ctk.CTkButton(app, text=t("view_orders"), fg_color=ORANGE, command=show_orders_frame).pack(pady=10)
    ctk.CTkButton(app, text=t("logout"), fg_color="gray", command=show_login_frame).pack(pady=30)

def show_form_frame():
    clear_frame()

    ctk.CTkLabel(app, text=t("event_form_title"), font=("Arial", 22, "bold"), text_color=ORANGE).pack(pady=15)

    event_type_var = ctk.StringVar(value=t("festival"))
    event_options = [t("festival"), t("wedding"), t("conference"), t("other")]
    ctk.CTkLabel(app, text=t("select_event_type")).pack(anchor="w", padx=20)
    ctk.CTkOptionMenu(app, values=event_options, variable=event_type_var).pack(padx=20, pady=5, fill="x")

    screen_type_var = ctk.StringVar(value=t("indoor"))
    screen_options = [t("indoor"), t("outdoor")]
    ctk.CTkLabel(app, text=t("screen_type")).pack(anchor="w", padx=20)
    ctk.CTkOptionMenu(app, values=screen_options, variable=screen_type_var).pack(padx=20, pady=5, fill="x")

    screen_size_entry = ctk.CTkEntry(app, placeholder_text=t("screen_size"))
    screen_size_entry.pack(padx=20, pady=5, fill="x")

    additional_entry = ctk.CTkEntry(app, placeholder_text=t("additional_requests"))
    additional_entry.pack(padx=20, pady=5, fill="x")

    def submit_order():
        event_type = event_type_var.get()
        screen_type = screen_type_var.get()
        screen_size = screen_size_entry.get().strip()
        additional = additional_entry.get().strip()

        if not screen_size:
            messagebox.showwarning("Input Error", t("missing_size"))
            return
        try:
            screen_size_val = float(screen_size)
        except:
            messagebox.showwarning("Input Error", t("invalid_size"))
            return

        confirm = messagebox.askyesno("Confirm", t("confirm_request"))
        if confirm:
            order = {
                "event_type": event_type,
                "screen_type": screen_type,
                "screen_size": screen_size_val,
                "additional": additional
            }
            orders_data[user_data["email"]]["orders"].append(order)
            save_orders(orders_data)

            subject = "New Techno Event Request"
            body = f"New request from {user_data['email']}:\nEvent: {event_type}\nScreen: {screen_type}\nSize: {screen_size_val} m²\nAdditional: {additional or 'N/A'}"
            send_email(subject, body)

            messagebox.showinfo("Success", t("submitted_msg"))
            show_main_menu()

    ctk.CTkButton(app, text=t("submit_order"), fg_color=ORANGE, command=submit_order).pack(pady=20)

def show_orders_frame():
    clear_frame()
    ctk.CTkLabel(app, text=t("my_orders"), font=("Arial", 22, "bold"), text_color=ORANGE).pack(pady=15)

    user_orders = orders_data.get(user_data["email"], {}).get("orders", [])
    if not user_orders:
        ctk.CTkLabel(app, text=t("no_orders")).pack(pady=20)
    else:
        for idx, order in enumerate(user_orders, 1):
            text = f"{idx}. {order['event_type']} - {order['screen_type']} - {order['screen_size']} m² - {order['additional'] or 'N/A'}"
            ctk.CTkLabel(app, text=text).pack(anchor="w", padx=20)

    ctk.CTkButton(app, text=t("back_to_menu"), fg_color=ORANGE, command=show_main_menu).pack(pady=20)

show_login_frame()
app.mainloop()
