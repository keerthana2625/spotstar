from django.contrib import admin
from django.urls import path
from app1 import views   # ✅ import your views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('upload-audio/', views.upload_audio, name='upload_audio'),
    path('upload-video/', views.upload_video, name='upload_video'),

    path('listener-audio/', views.listener_audio, name='listener_audio'),
    path('listener-video/', views.listener_video, name='listener_video'),

    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('search/', views.global_search, name='global_search'),

    path('media/<int:media_id>/', views.media_detail, name='media_detail'),
    path('media/<int:media_id>/like/', views.toggle_like, name='toggle_like'),
    path('media/<int:media_id>/comment/', views.add_comment, name='add_comment'),
    path('creator/<str:username>/', views.creator_profile, name='creator_profile'),
    path('liked-media/', views.liked_media, name='liked_media'),
    path('playlists/', views.playlists, name='playlists'),
    path('playlist/add/<int:media_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('playlist/remove/<int:playlist_id>/<int:media_id>/', views.remove_from_playlist, name='remove_from_playlist'),
    path('settings/', views.settings_view, name='settings'),

    path('logout/', views.logout, name='logout'),
]

# MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)