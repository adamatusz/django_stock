from django.urls import path
from quotes import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('add_stock/', views.add_stock, name="add_stock"),
    path('delete/<stock_id>/', views.delete, name="delete"),
    path('delete_stock/', views.delete_stock, name="delete_stock"),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(), name="login"),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name="logout"),
]