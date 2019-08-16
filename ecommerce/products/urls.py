from django.urls import path
from products.views import ProductListView,ProductDetailFeaturedView
#ProductDetailView,ProductListFeaturedView
urlpatterns = [
    #path('', views.homepage,name="homepage"),
    path('',ProductListView.as_view(),name="products"),
    #path('products/<int:pk>/',ProductDetailView.as_view(),name="productsde"),
    #path('products-fe/',ProductListFeaturedView.as_view(),name="productsfeatured"),
    path('<str:slug>/',ProductDetailFeaturedView.as_view(),name="productsdetailfeatured"),
]
