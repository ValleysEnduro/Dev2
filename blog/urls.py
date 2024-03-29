from django.urls import path
from .views import post_list, post_detail
from . import views

# blog/urls.py
urlpatterns = [
    # Other patterns...
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]

