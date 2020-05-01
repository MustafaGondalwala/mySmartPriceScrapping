from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('autosuggestion',views.autosuggestion,name="autosuggestion"),
    path('product-listing',views.product_search,name="product_search"),
    path('get-product',views.get_product,name="get_product"),
    path('get-links',views.get_links,name="get_links"),
    path('specific-product',views.specific_product,name="specific_product"),
]