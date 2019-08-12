from django.urls import path
from products.views import ProductListView,ProductDetailView
urlpatterns = [
    #path('', views.homepage,name="homepage"),
    path('products/',ProductListView.as_view(),name="products"),
    path('products/<int:pk>/',ProductDetailView.as_view(),name="productsde"),
   
]
