from django.urls import path

from . import views

app_name = "backend"

urlpatterns = [
    path('', views.index, name="index"),
    path('users/register', views.RegisterView.as_view(), name="register"),
    path('users/login', views.LoginView.as_view(), name="login"),
    path('users/logout', views.logout_view, name="logout"),
    path('user/profile/', views.profile, name="profile"),
]
