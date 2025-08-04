from django.db import models
from products.models import Product
from django.core.validators import MinValueValidator
from accounts.models import CustomUser
# Create your models here.



class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="کاربر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"

    def __str__(self):
        return f"سبد خرید کاربر {self.user.username}"

    def get_total_price(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="سبد خرید")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="تعداد")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} در سبد"

    def get_subtotal(self):
        return self.quantity * self.product.price

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار'),
        ('pending_payment', 'در انتظار پرداخت'),  # گزینه جدید
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('cancelled', 'لغو شده'),
    )
    PAYMENT_METHODS = (
        ('online', 'پرداخت آنلاین'),
        ('cod', 'پرداخت در محل'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('unpaid', 'پرداخت نشده'),
        ('paid', 'پرداخت شده'),
        ('failed', 'ناموفق'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="کاربر")
    recipient_name = models.CharField(max_length=100, verbose_name="نام تحویل‌گیرنده")
    address = models.TextField(verbose_name="آدرس")
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تماس")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cod', verbose_name="روش پرداخت")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid', verbose_name="وضعیت پرداخت")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")
    tracking_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="کد رهگیری")
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="شماره پیگیری پرداخت")
    receipt_image = models.ImageField(upload_to='receipts/%Y/%m/%d/', blank=True, null=True, verbose_name="تصویر رسید پرداخت")
    total_price = models.PositiveIntegerField(verbose_name="مجموع قیمت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
        ordering = ['-created_at']

    def __str__(self):
        return f"سفارش {self.id} - کاربر {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="تعداد")
    price = models.PositiveIntegerField(verbose_name="قیمت واحد")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self):
        return f"{self.quantity} x {self.product.name} در سفارش {self.order.id}"

    def get_subtotal(self):
        return self.quantity * self.price