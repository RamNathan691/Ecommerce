from django.shortcuts import render
#from django.views import ListView
from . models import Product
from django.http import  Http404
from django.views.generic import ListView,DetailView



class ProductListView(ListView):
    queryset=Product.objects.all()
    template_name='products/productslist.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView,self).get_context_data(**kwargs)
       
        return context
    def get_queryset(self,*args,**kwargs):
        request=self.request
        return Product.objects.all()
        
    
    
class ProductDetailView(DetailView):
    queryset=Product.objects.all()
    template_name='products/productsdetail.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        print(context)
        return context
    def get_object(self,*args,**kwargs):
        request=self.request
        pk=self.kwargs.get('pk')
        instance=Product.objects.get_byˍid(pk)
        if instance is None:
             raise Http404("product doesnt exist")
        return instance

    
