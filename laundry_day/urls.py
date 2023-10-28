from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("user/<int:pk>", views.UserDetailView.as_view(), name="user_detail")
]
