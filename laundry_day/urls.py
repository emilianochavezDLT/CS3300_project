from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("user/<int:pk>", views.UserDetailView.as_view(), name="user_detail"),
    path('user/<int:pk>/createlaundryrequest', views.create_laundry_request, name='create_laundry_request'),
    path('user/<int:from_user_id>/mylaundryrequest', views.laundry_request_detail, name='laundry_request_detail'),
]   
