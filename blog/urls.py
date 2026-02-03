from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('search/', views.search_posts, name='search'),

    # User URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    
    # Comment URL
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),

    path('create/', views.create_post, name='create_post'),

    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    
]