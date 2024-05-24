from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),
    path('buying/', views.buying_view, name='buying'),
    path('courses/', views.courses_view, name='courses'),
    path('profile/', views.profile_view, name='profile'),
]
