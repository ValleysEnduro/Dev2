from django.urls import path
from .views import post_list, post_detail
from . import views

urlpatterns = [
    path('', post_list, name='post_list'),
    # Updating the path to use slugs
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]
