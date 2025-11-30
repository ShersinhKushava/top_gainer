from django.urls import path
from . import views
from .views import top_gainers

urlpatterns = [
    path('stocks/', views.stock_list, name='stock-list'),
    path('stocks/<str:pk>/', views.stock_detail, name='stock-detail'),
    path('top-gainers/', top_gainers, name='top-gainers'),
  
]
