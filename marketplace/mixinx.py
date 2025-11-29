from marketplace.models import Product
from django.http.response import HttpResponse
from django.http import Http404

class ProductExistRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if Product.objects.filter(id=pk, is_active=True):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionError("Permission Error: Product not active.")
        
class StockRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.stock < 1:
            raise Http404('This product not found.')
        
        return super().dispatch(request, *args, **kwargs)