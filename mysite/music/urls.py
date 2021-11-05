from django.urls import path
from . import views

app_name = "music"   
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("pricing/", views.pricing, name='pricing')
]