# 🛍️ Divine Beauty Online Store

## 🇮🇷 فروشگاه آنلاین Divine Beauty

این پروژه یک **وب اپلیکیشن فروشگاه آنلاین** است که با استفاده از **Django** توسعه داده شده و امکانات کاملی را برای خرید آنلاین محصولات زیبایی فراهم می‌کند. رابط کاربری روان و فارسی، پشتیبانی از اسلاگ‌های فارسی و قابلیت‌های مختلف مثل مدیریت سبد خرید و سفارش‌ها، تجربه‌ی خرید راحتی را برای کاربران فراهم کرده است.

---

### ✨ ویژگی‌ها

- **مدیریت محصولات**: نمایش محصولات با نام، قیمت، توضیحات و موجودی – پشتیبانی کامل از اسلاگ‌های فارسی.
- **سبد خرید پویا**: امکان افزودن، حذف و به‌روزرسانی آیتم‌ها در سبد خرید.
- **سفارش و پرداخت**: ثبت سفارش با انتخاب نوع پرداخت (آنلاین یا پرداخت در محل) و اطلاعات ارسال.
- **حساب کاربری**: ثبت‌نام، ورود، خروج و مشاهده‌ی پروفایل با تاریخچه سفارش‌ها و وضعیت سبد خرید.
- **پشتیبانی کامل از زبان فارسی** در رابط کاربری و محتوای سایت.
- **پیام‌رسانی تعاملی** با استفاده از `django.contrib.messages`.

---

### 🛠 تکنولوژی‌ها

- **زبان برنامه‌نویسی**: Python 3.x  
- **فریم‌ورک وب**: Django 4.x  
- **دیتابیس**: PostgreSQL  
- **فرانت‌اند**: HTML, CSS, Tailwind CSS, JavaScript  
- **فونت‌ها**: Zain، Jost (فارسی)  
- **کتابخانه‌ها**:  
  - `django.contrib.auth`: مدیریت کاربران  
  - `django.contrib.messages`: نمایش پیام‌ها  

---

### 📦 پیش‌نیازها

- Python 3.8 یا بالاتر  
- Django 4.x  
- virtualenv (اختیاری برای ساخت محیط مجازی)  
- مرورگر مدرن  

---

### ⚙️ نصب و اجرا

```bash
# کلون کردن پروژه
git clone https://github.com/Sajjadhosseinrezaei/DivineBeautyShop.git
cd DivineBeautyShop

# ایجاد محیط مجازی
python -m venv venv
source venv/bin/activate  # در ویندوز: venv\Scripts\activate

# نصب وابستگی‌ها
pip install -r requirements.txt

# اعمال مایگریشن‌ها
python manage.py makemigrations
python manage.py migrate

# جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic

# ایجاد سوپریوزر (اختیاری)
python manage.py createsuperuser

# اجرای سرور
python manage.py runserver
```

> 📍 پروژه روی `http://127.0.0.1:8000` در حال اجرا خواهد بود.

---

### 🗂 ساختار پروژه

```
DivineBeautyShop/
├── accounts/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── orders/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── products/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── templates/
├── static/
```

---

### 🌐 مسیرهای کلیدی

- `/` : صفحه اصلی  
- `/list/` : لیست محصولات  
- `/products/<id>/` : جزئیات محصول  
- `/cart/` : سبد خرید  
- `/cart/add/<id>/` : افزودن به سبد  
- `/order/create/` : ثبت سفارش  
- `/order/<pk>/` : مشاهده سفارش  
- `/accounts/register/` : ثبت‌نام  
- `/accounts/login/` : ورود  
- `/accounts/logout/` : خروج  
- `/accounts/profile/` : پروفایل  

---

### 💡 نکات مهم

- **مدیریت موجودی**: بررسی موجودی قبل از افزودن به سبد یا ثبت سفارش.  
- **نمایش پیام‌ها**: پیام‌های موفقیت/خطا با `django.contrib.messages`.

---

### 🚀 توسعه‌های آینده

- اتصال درگاه پرداخت آنلاین  
- رابط کاربری تعاملی‌تر با انیمیشن  
- فیلترهای پیشرفته برای جستجوی محصولات  
- تخفیف و سیستم کد تخفیف (Promocode)  
- اعتبارسنجی حرفه‌ای فرم‌ها  

---

### 🤝 مشارکت

برای مشارکت لطفاً یک issue باز کنید یا pull request بفرستید. در صورت مشاهده باگ، مخصوصاً در مسیرهای redirect، لطفاً با جزئیات گزارش دهید.

---

### 📧 تماس

- توسعه‌دهنده: **sajjadhossein**  
- ایمیل: [sajjadhosseinrezaei@yahoo.com](mailto:sajjadhosseinrezaei@yahoo.com)

---

## 🇬🇧 English Version

### ✨ Features

- **Product Management**: View name, price, description, stock – with Persian slug support.
- **Dynamic Cart**: Add, update, remove items.
- **Order & Payment**: Create order with shipping info and payment method.
- **User Account**: Register, login, logout, profile with cart/order history.
- **Fully Persian-compatible UI**.
- **Django messages** for notifications.

### 🛠 Technologies

- Python 3.x  
- Django 4.x  
- PostgreSQL  
- HTML, CSS, Tailwind CSS, JavaScript  
- Fonts: Zain, Jost  
- Libraries: `django.contrib.auth`, `django.contrib.messages`  

### ⚙️ Installation

```bash
git clone https://github.com/Sajjadhosseinrezaei/DivineBeautyShop.git
cd DivineBeautyShop

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

python manage.py createsuperuser  # optional
python manage.py runserver
```

> 📍 App will be available at `http://127.0.0.1:8000`

### 🗂 Structure

```
DivineBeautyShop/
├── accounts/
├── orders/
├── products/
├── templates/
├── static/
```

### 🌐 URLs

- `/`, `/list/`, `/products/<id>/`, `/cart/`, `/order/create/`, `/accounts/...`

### 🚀 Future

- Online payment  
- Animated UI improvements  
- Advanced filters  
- Promo codes  
- Better form validation  

### 📧 Contact

**sajjadhossein** — [sajjadhosseinrezaei@yahoo.com](mailto:sajjadhosseinrezaei@yahoo.com)
