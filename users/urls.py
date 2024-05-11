# users/urls.py
from django.urls import path
from .views import (
    register_view, register_user, login_view, perform_login,
    logout_view, perform_logout, dashboard, profile_view,
    update_avatar_view, update_avatar, delete_avatar, redirect_to_profile,
    confirm_cancel_entry, cancel_entry
)

app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register_view'),
    path('register/submit/', register_user, name='register_user'),
    path('login/', login_view, name='login_view'),
    path('login/submit/', perform_login, name='perform_login'),
    path('logout/', logout_view, name='logout_view'),
    path('logout/submit/', perform_logout, name='perform_logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile_view, name='profile_view'),
    path('avatar/update/', update_avatar_view, name='update_avatar_view'),
    path('avatar/update/submit/', update_avatar, name='update_avatar'),
    path('avatar/delete/', delete_avatar, name='delete_avatar'),
    path('redirect_to_profile/', redirect_to_profile, name='redirect_to_profile'),
    path('entry/confirm_cancel/<int:entry_id>/', confirm_cancel_entry, name='confirm_cancel_entry'),
    path('entry/cancel/<int:entry_id>/', cancel_entry, name='cancel_entry'),
]
