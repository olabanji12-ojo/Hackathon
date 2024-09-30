from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('login_page/', views.login_page, name='login_page'),
    path('logout_page/', views.logout_page, name='logout_page'),
    path('register_page/', views.register_page, name='register_page'),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('processOrder/', views.processOrder, name='processOrder'),
    
    

]