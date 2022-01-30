from django.urls import path

from . import views

app_name = "backend"

urlpatterns = [
    path('', views.index, name="index"),
    path('users/register', views.RegisterView.as_view(), name="register"),
    path('users/login', views.LoginView.as_view(), name="login"),
    path('users/logout', views.logout_view, name="logout"),
    path('user/profile/', views.profile, name="profile"),
    path('market/<str:code>', views.market, name="market"),
    path('shops/', views.shop, name="shops"),
    path('shop/buy/<int:id>/<str:color>', views.buy, name="buy"),
    path('item/sell/<int:id>/<str:color>', views.sell, name="sell"),

    #REST API
    path('game/user/<str:identifier>', views.UserDetail.as_view()),
]
