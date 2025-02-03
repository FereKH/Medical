import streamlit as st
import pandas as pd
import sqlite3
from PIL import Image

# ایجاد ارتباط با پایگاه داده SQLite
conn = sqlite3.connect("patients.db")
c = conn.cursor()

# ایجاد جدول اگر وجود نداشته باشد
c.execute("""
CREATE TABLE IF NOT EXISTS patients (
    name TEXT,
    status TEXT,
    doctor TEXT,
    imaging_center TEXT,
    diagnosis TEXT,
    notes TEXT,
    analysis_file TEXT
)
""")
conn.commit()

# تابع برای اضافه کردن ورودی بیمار
def add_patient(name, status, doctor, imaging_center, diagnosis, notes, analysis_file):
    c.execute("INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?)", 
              (name, status, doctor, imaging_center, diagnosis, notes, analysis_file))
    conn.commit()

# تابع برای حذف ورودی بیمار
def delete_patient(name):
    c.execute("DELETE FROM patients WHERE name = ?", (name,))
    conn.commit()

# اپلیکیشن Streamlit
st.set_page_config(layout="wide")

# بارگذاری تصویر لوگو
st.image("D:/RandD/brochures/MSAlipour/KIO_new_LOGO.png", width=100)

# بارگذاری تصویر پس‌زمینه
background_image = Image.open("D:/RandD/medica-background3.jpg")
st.image(background_image, use_container_width=True)  # استفاده از use_container_width

# تنظیم رنگ پس‌زمینه
st.markdown("""
    <style>
        .main-header {
            padding: 20px;
            text-align: center;
            color: white;
            font-size: 30px;
            font-weight: bold;
            background-color: rgba(30, 90, 109, 0.7); /* رنگ سازمانی */
        }
        body {
            color: white;
            text-align: right; /* راست‌چین */
            direction: rtl; /* راست‌چین */
        }
    </style>
""", unsafe_allow_html=True)

# عنوان اصلی
st.markdown("<div class='main-header'>سیستم مدیریت کارهای پزشکی</div>", unsafe_allow_html=True)

# ورودی نام بیمار
patient_name = st.text_input("لطفاً نام بیمار را وارد کنید:")

if patient_name:
    # نمایش داده‌های بیماران
    st.subheader("پیگیری کارهای بیمار")
    df = pd.read_sql(f"SELECT * FROM patients WHERE name = '{patient_name}'", conn)

    if not df.empty:
        st.dataframe(df)

        # بخش برای حذف بیمار
        if st.button("حذف بیمار"):
            delete_patient(patient_name)
            st.success(f"بیمار {patient_name} با موفقیت حذف شد.")
    else:
        st.write("هیچ داده‌ای برای این بیمار موجود نیست.")

    # نوار کناری برای ورود بیمار جدید
    st.sidebar.header("اضافه کردن بیمار جدید")
    name = st.sidebar.text_input("نام بیمار")
    status = st.sidebar.selectbox("وضعیت", ["ارجاع داده شده", "برنامه‌ریزی شده", "تصویر برداری انجام شده", "تحلیل انجام شده", "بررسی شده", "مشاوره پزشک"])
    doctor = st.sidebar.text_input("نام پزشک")
    imaging_center = st.sidebar.text_input("مرکز تصویر برداری")
    diagnosis = st.sidebar.text_area("تشخیص")
    notes = st.sidebar.text_area("یادداشت‌ها")
    analysis_file = st.sidebar.text_input("لینک فایل تحلیل (اختیاری)")

    if st.sidebar.button("اضافه کردن بیمار"):
        add_patient(name, status, doctor, imaging_center, diagnosis, notes, analysis_file)
        st.sidebar.success("بیمار با موفقیت اضافه شد.")

# بستن ارتباط با پایگاه داده
conn.close()