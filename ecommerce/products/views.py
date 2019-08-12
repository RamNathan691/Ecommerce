from django.shortcuts import render
#from django.views import ListView
from . models import Product
from django.views.generic import ListView,DetailView



class ProductListView(ListView):
    queryset=Product.objects.all()
    template_name='products/productslist.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView,self).get_context_data(**kwargs)
       
        return context
    

class ProductDetailView(DetailView):
    queryset=Product.objects.all()
    template_name='products/productsdetail.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        print(context)
        return context
        
