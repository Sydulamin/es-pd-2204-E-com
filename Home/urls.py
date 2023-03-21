from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="Home"),
    path('profile/', views.profile, name="profile")
]
