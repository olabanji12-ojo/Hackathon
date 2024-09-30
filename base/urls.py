from django.urls import path
from .import views
import uuid

urlpatterns = [
    path('', views.home, name='home'),
    path('event/<uuid:id>/', views.event, name='event'),
    path('profile/<uuid:id>/', views.profile, name='profile'),
    path('account/', views.account, name='account'),
    path('event_confirmation/<uuid:id>/', views.event_confirmation, name='event_confirmation'),
    path('submit_form/<uuid:id>/', views.submit_form, name='submit_form'),
    path('update_form/<uuid:id>/', views.update_form, name='update_form'),
    path('login_page/', views.login_page, name='login_page'),
    path('logout_page/', views.logout_page, name='logout_page'),
    path('register_page/', views.register_page, name='register_page'),
    
]
