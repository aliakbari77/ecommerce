from django.shortcuts import render
from marketplace.models import Product

# Create your views here.
def products_list(request):
    products = Product.objects.prefetch_related('vendor').all()
    return render(request, 'products_list.html', {
        'products': products
    })