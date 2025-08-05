from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem
from products.models import Category, Product



class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'get_subtotal')
    readonly_fields = ('get_subtotal',)

    def get_subtotal(self, obj):
        return obj.get_subtotal()
    get_subtotal.short_description = 'زیرمجموعه'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_items', 'get_total_price', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email',)  # استفاده از email به جای username
    inlines = [CartItemInline]
    readonly_fields = ('get_total_items', 'get_total_price', 'created_at', 'updated_at')

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'تعداد آیتم‌ها'

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'مجموع قیمت'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price', 'get_subtotal')
    readonly_fields = ('get_subtotal',)

    def get_subtotal(self, obj):
        return obj.get_subtotal()
    get_subtotal.short_description = 'زیرمجموعه'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_method', 'payment_status', 'total_price', 'created_at', 'updated_at')
    list_filter = ('status', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('id', 'user__email', 'recipient_name')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status', 'payment_status')
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'get_subtotal', 'created_at', 'updated_at')
    list_filter = ('product', 'created_at')
    search_fields = ('product__name', 'cart__user__email')
    readonly_fields = ('get_subtotal', 'created_at', 'updated_at')

    def get_subtotal(self, obj):
        return obj.get_subtotal()
    get_subtotal.short_description = 'زیرمجموعه'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'get_subtotal')
    list_filter = ('product',)
    search_fields = ('product__name', 'order__id')
    readonly_fields = ('get_subtotal',)

    def get_subtotal(self, obj):
        return obj.get_subtotal()
    get_subtotal.short_description = 'زیرمجموعه'

