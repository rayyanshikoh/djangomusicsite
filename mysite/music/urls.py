from django.urls import path
from . import views

app_name = "music"   
urlpatterns = [
    path("home/", views.homepage, name="homepage"),
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("pricing/", views.pricing, name='pricing'),
    path("upload/", views.simple_upload, name="upload")
]