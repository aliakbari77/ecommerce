from django.shortcuts import render
from marketplace.mixinx import ProductExistRequiredMixin, StockRequiredMixin
from marketplace.models import Product
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from account.models import User

# Create your views here.
def products_list(request):
    products = Product.objects.prefetch_related('vendor').all()
    return render(request, 'products_list.html', {
        'products': products
    })

class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = 'product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['vendors'] = User.objects.filter(is_vendor=True)

        print(context.keys())
        return context
    
    def get_queryset(self):
        self.queryset = Product.objects.all()
        return super().get_queryset()


class ProductDetailView(StockRequiredMixin, DetailView):
    template_name = 'product_detail.html'
    
    def get_queryset(self):
        self.queryset = Product.objects.all()
        return super().get_queryset()
