from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from basket import views

urlpatterns = [
    path('trade/', views.TradeList.as_view(), name='trades'),
    path('portfolio/',views.PortfolioList.as_view(), name='portfolios'),
    #path('trade/<int:pk>/', views.trade_detail),
]