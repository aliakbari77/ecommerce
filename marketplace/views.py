from django.shortcuts import render
from marketplace.forms import ContactForm, ProductForm
from marketplace.mixinx import ProductExistRequiredMixin, StockRequiredMixin
from marketplace.models import Product
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from account.models import User
from django.views.generic import FormView, CreateView, UpdateView, DeleteView

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


class ContactFormView(FormView):
    template_name = 'contact_form.html'
    form_class = ContactForm
    success_url = '/product-detail/1/'

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')

        print(f'{message} received from Name: {name}, Email: {email}')

        return super().form_valid(form)
    

class ProductCreateFormView(CreateView):
    model = Product
    template_name = 'product_form.html'
    form_class = ProductForm
    success_url = '/products-list/'


class ProductUpdateFormView(UpdateView):
    model = Product
    template_name = 'product_form.html'
    form_class = ProductForm
    success_url = '/products-list/'


class ProductDeleteFormView(DeleteView):
    model = Product
    success_url = '/products-list/'
    template_name = 'confirm_delete.html'

