from django.contrib.auth import views as auth_views  # Hakikisha hii ipo
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URLs za user authentication
    path('accounts/login/', views.loginPage, name="login"),  # URL ya login
    path('accounts/logout/', views.logoutUser, name="logout"),  # URL ya logout
    path('accounts/register/', views.registerPage, name="register"),  # URL ya register

    # URLs za room na profile
    path('', views.home, name='home'),
    path('room/<int:pk>/', views.room, name='room'),
    path('profile/<int:pk>/', views.userprofile, name='user-profile'),
    path('create-room/', views.createroom, name='create-room'),
    path('update-room/<int:pk>/', views.update_room, name='update_room'),
    path('delete-room/<int:pk>/', views.delete_room, name='delete_room'),
    path('delete-message/<int:pk>/', views.deleteMessage, name='delete_message'),
    path('update-user/', views.updateUser, name='update-user'),
    path('topics.html/', views.topicsPage, name='topics'),

    # URL mpya za kutuma ujumbe
    path('send-message/<int:room_id>/', views.send_message, name='send_message'),
    
    # Activity page
    path('activity/activity', views.activityPage, name='activity'),

    # URLs za password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# Kuwezesha upakiaji wa media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
