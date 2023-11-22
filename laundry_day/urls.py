from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("user/<int:pk>", views.UserDetailView.as_view(), name="user_detail"),
    path('user/<int:pk>/createlaundryrequest', views.create_laundry_request, name='create_laundry_request'),
    path('user/<int:from_user_id>/laundryrequestdetail', views.laundry_request_detail, name='laundry_request_detail'),
    path('user/<int:from_user_id>/<int:pk>/updatelaundryrequest', views.update_laundry_request, name='update_laundry_request'),
    path('user/<int:pk>/deletelaundryrequest', views.delete_laundry_request, name='delete_laundry_request'),
    path('users/', views.UserListView.as_view(), name='users_list'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
]   
