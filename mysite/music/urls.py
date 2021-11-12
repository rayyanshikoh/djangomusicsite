from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "music"   
urlpatterns = [
    path("home/", views.homepage, name="homepage"),
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("pricing/", views.pricing, name='pricing'),
    path("upload/", views.simple_upload, name="upload"),
    path("artist/", views.artists, name="artists"),
    path('<int:artist_id>/', views.albums, name='albums'),
    path('<int:artist_id>/<int:album_id>', views.songs, name='songs')
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
