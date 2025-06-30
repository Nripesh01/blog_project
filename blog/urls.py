from django.urls import path
from blog import views


urlpatterns = [
    path('list/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('', views.post_login, name='post_login'),
    path('logout/', views.post_logout, name='post_logout'),
    path('register/', views.post_register, name='post_register'),
]
