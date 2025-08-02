from django.views.generic import ListView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'products/html/product_list.html'  # مسیر تمپلیت شما
    context_object_name = 'products'  # نامی که توی تمپلیت استفاده می‌شه
    paginate_by = 8  # تعداد محصولات در هر صفحه

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        # فیلتر اختیاری برای دسته‌بندی (اگه بعداً اضافه کردید)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # اضافه کردن داده‌های اضافی مثل دسته‌بندی‌ها یا محصولات ویژه
        context['featured_products'] = Product.objects.filter(is_featured=True, is_available=True)[:4]
        return context