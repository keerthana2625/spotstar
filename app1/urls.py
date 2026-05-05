from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('upload-audio/', views.upload_audio, name='upload_audio'),
    path('upload-video/', views.upload_video, name='upload_video'),

    path('listener-audio/', views.listener_audio, name='listener_audio'),
    path('listener-video/', views.listener_video, name='listener_video'),

    path('logout/', views.logout, name='logout'),
]
path('admin-panel/', views.admin_panel, name='admin_panel'),
path('approve/<int:id>/', views.approve, name='approve'),
path('reject/<int:id>/', views.reject, name='reject'),