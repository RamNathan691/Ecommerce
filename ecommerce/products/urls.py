from django.urls import path
from products.views import ProductListView,ProductDetailView,ProductDetailFeaturedView,ProductListFeaturedView
urlpatterns = [
    #path('', views.homepage,name="homepage"),
    path('products/',ProductListView.as_view(),name="products"),
    path('products/<int:pk>/',ProductDetailView.as_view(),name="productsde"),
    path('products-fe/',ProductListFeaturedView.as_view(),name="productsfeatured"),
    path('products-fe/<str:slug>/',ProductDetailFeaturedView.as_view(),name="productsdetailfeatured"),
]
