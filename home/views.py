from django.shortcuts import render
from django.views.generic import TemplateView
from products.models import Category, Product
from django.db.models import Sum



class HomeView(TemplateView):
    template_name = 'home/html/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(is_active=True, parent__isnull=True)
        context['categories'] = categories
        context['bestsellers'] = Product.objects.filter(is_available=True).annotate(
            total_sold=Sum('orderitem__quantity')
        ).order_by('-total_sold')[:5]
        return context
