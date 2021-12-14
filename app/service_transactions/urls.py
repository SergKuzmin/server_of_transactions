from django.urls import path

from . import views

urlpatterns = [
    path('account', views.AccountsView.as_view()),
    path(r'account/<str:pk>/', views.AccountView.as_view()),
    path('transaction', views.TransactionsView.as_view())
]
