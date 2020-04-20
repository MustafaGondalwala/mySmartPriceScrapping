from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('autosuggestion',views.autosuggestion,name="autosuggestion"),
    path('product_search',views.product_search,name="product_search"),
    path('get-product-by-link',views.get_search_by_link,name="get_search_by_link"),


]