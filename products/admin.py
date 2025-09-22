from django.contrib import admin
from .models import Category, Product
from mptt.admin import DraggableMPTTAdmin
# Register your models here.


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',       # آیکون باز و بسته شدن درخت
        'indented_title',     # نمایش تو در توی دسته‌بندی‌ها
        'parent',
        'is_active',
        'display_order',      # ترتیب نمایش
        'created_at',
    )
    list_editable = ('display_order', 'is_active')  # ویرایش سریع
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    exclude = ('slug',)  # مخفی کردن فیلد slug در فرم ادمین
    list_display_links = ('indented_title',)  # کلیک روی اسم دسته برای ورود به ویرایش


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'is_featured', 'created_at']
    list_filter = ['is_available', 'is_featured', 'category', 'created_at']
    search_fields = ['name', 'description']
    exclude = ['slug']  # مخفی کردن فیلد slug در فرم ادمین
    list_editable = ['is_available', 'is_featured']
