from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.landingPage, name = 'landing-page'),
    path('home/', views.home, name = 'home'),
    path('login/', views.loginUser, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.registerUser, name = "register"),
    path('create/', views.createBlog, name='create-blog'),
    path('read/<str:blogID>/', views.readBlog, name='read-blog'),
    path('like/<str:blogID>/', views.likeBlog, name='like-blog'),
    path('profile/<str:userID>/', views.viewProfile, name='view-profile'),
    path('edit-profile/', views.editProfile, name='edit-profile'),


]

