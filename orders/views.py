from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from django.views import View


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/html/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        return context

class CartAddView(LoginRequiredMixin, View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        quantity = int(request.POST.get('quantity', 1))
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        if cart_item.quantity > product.stock:
            messages.error(request, f"موجودی کافی نیست. حداکثر {product.stock} عدد موجود است.")

            cart_item.quantity = product.stock
            cart_item.save()
            return redirect('orders:cart')
        
        cart_item.save()
        messages.success(request, f"{product.name} به سبد خرید اضافه شد.")
        return redirect('orders:cart')

class CartUpdateView(LoginRequiredMixin, View):
    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, f"{cart_item.product.name} از سبد خرید حذف شد.")
        else:
            if quantity <= cart_item.product.stock:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, f"تعداد {cart_item.product.name} به‌روزرسانی شد.")
            else:
                messages.error(request, f"موجودی کافی نیست. حداکثر {cart_item.product.stock} عدد موجود است.")
        return redirect('orders:cart')

class CartRemoveView(LoginRequiredMixin, View):
    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f"{product_name} از سبد خرید حذف شد.")
        return redirect('orders:cart')

class OrderCreateView(LoginRequiredMixin, View):
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            messages.error(request, "سبد خرید شما خالی است.")
            return redirect('orders:cart')

        recipient_name = request.POST.get('recipient_name')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')
        phone_number = request.POST.get('phone_number')
        payment_method = request.POST.get('payment_method')

        if not all([recipient_name, address, postal_code, phone_number, payment_method]):
            messages.error(request, "لطفاً تمام فیلدهای اطلاعات ارسال را پر کنید.")
            return redirect('orders:cart')

        order = Order.objects.create(
            user=request.user,
            recipient_name=recipient_name,
            address=address,
            postal_code=postal_code,
            phone_number=phone_number,
            payment_method=payment_method,
            status='pending_payment' if payment_method == 'online' else 'pending',
            total_price=cart.get_total_price()
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()

        cart.items.all().delete()
        messages.success(request, f"سفارش شما با شماره {order.id} ثبت شد.")
        if order.payment_method == 'online':
            return redirect('orders:order_pay', order_id=order.id)
        return redirect('orders:order_detail', pk=order.id)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/html/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderPayView(LoginRequiredMixin, View):
    template_name = 'orders/html/order_pay.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.payment_status != 'unpaid' or order.status != 'pending_payment':
            messages.error(request, "این سفارش در حال حاضر قابل پرداخت نیست.")
            return redirect('orders:order_detail', pk=order.id)
        return render(request, self.template_name, {'order': order})

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.payment_status != 'unpaid' or order.status != 'pending_payment':
            messages.error(request, "این سفارش در حال حاضر قابل پرداخت نیست.")
            return redirect('orders:order_detail', pk=order.id)

        transaction_id = request.POST.get('transaction_id')
        receipt_image = request.FILES.get('receipt_image')

        if not transaction_id:
            messages.error(request, "شماره پیگیری پرداخت الزامی است.")
            return redirect('orders:order_pay', order_id=order.id)

        order.transaction_id = transaction_id
        if receipt_image:
            order.receipt_image = receipt_image
        order.payment_status = 'paid'
        order.status = 'waiting_admin'
        order.save()

        messages.success(request, f"پرداخت سفارش {order.id} ثبت شد و در حال بررسی است.")
        return redirect('orders:order_detail', pk=order.id)
