
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('interested_races/', views.interested_races, name='interested_races'),
    path('registered_races/', views.registered_races, name='registered_races'),
    path('races_created/', views.races_created, name='races_created'),
    path('registration_user/', views.registration_user, name='registration_user'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('insert_user/', views.insert_user, name='insert_user'),
    path('accounts/', include('django.contrib.auth.urls')),
]
