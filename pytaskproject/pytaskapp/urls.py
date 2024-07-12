from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_user, name="add_user"),
    path("read/", views.read_users, name="read_users"),
]
