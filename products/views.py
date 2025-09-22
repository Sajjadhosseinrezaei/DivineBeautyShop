from django.views.generic import ListView, TemplateView, DetailView
from .models import Product, Category
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from products.models import Product, Category

class ProductListView(ListView):
    model = Product
    template_name = 'products/html/product_list.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        qs = Product.objects.filter(is_available=True).order_by('-created_at')
        category_id = self.kwargs.get('id')
        sub_id = self.request.GET.get('sub')  # ← زیر دسته از query param

        if category_id:
            try:
                category = Category.objects.get(id=category_id)

                if sub_id and sub_id != "all":
                    # فقط زیر دسته انتخاب شده
                    qs = qs.filter(category__id=sub_id)
                else:
                    # همه محصولات دسته والد و زیر دسته‌ها
                    descendant_ids = category.get_descendants(include_self=True).values_list('id', flat=True)
                    qs = qs.filter(category__id__in=descendant_ids)
            except Category.DoesNotExist:
                pass

        return qs.select_related('category')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('id')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                context['category'] = category
                context['children'] = category.get_children()
            except Category.DoesNotExist:
                context['category'] = None
        else:
            context['category'] = None

        context['featured_products'] = (
            Product.objects
            .filter(is_featured=True, is_available=True)
            .order_by('-created_at')[:4]
        )
        return context



class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/html/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return get_object_or_404(Product, id=id)