from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterCreationForm
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
import json
import datetime

# Create your views here.

def store(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_item' : 0, 'shipping' : False}
        cartItems = order['get_cart_item']    
    
    
    q = request.GET.get('q')
    if q != None:
        products = Products.objects.filter(product_name__icontains=q)
    else:
        products = Products.objects.all()
    
    page = request.GET.get('page')
    result = 3
    paginator = Paginator(products, result)
    
    try:
        products = paginator.page(page)
        
    except PageNotAnInteger:
        page = 1
        products = paginator.page(page)
      
    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)
        
    
    
    context = {
        'products' : products, 'paginator' : paginator, 'cartItems': cartItems
        
        }
    
    return render(request, 'store/store.html', context)
    
    
    class Meta:
        ordering = [created]

    
   
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_item' : 0, 'shipping' : False}
        cartItems = order['get_cart_item']
    
    context = {'items' : items, 'order' : order, 'cartItems' : cartItems }
    return render(request, 'store/cart.html', context)
        
    
	

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_item' : 0, 'shipping' : False}
        cartItems = order['get_cart_item']
    
    
    context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
    return render(request, 'store/checkout.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user based on username and password
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            return redirect('store')
        else:
            # If authentication fails, return an error
            messages.error(request, 'Username or password is not correct')

    return render(request, 'store/login_page.html')
    

def logout_page(request):
    
    logout(request)
  
    return render(request, 'store/login_page.html')


def register_page(request):
    form = RegisterCreationForm()
    if request.method == 'POST':
        form = RegisterCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'an error occured during registeration')
    
    context = {'form' : form}
    return render(request, 'store/register_page.html', context)


def updateItem(request):
    
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:',action )
    print('Action:',productId )
    
    customer = request.user.customer
    product = Products.objects.get(id= productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        
        
        
    return JsonResponse('item was added', safe=False)



def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
       customer = request.user.customer
       order, created = Order.objects.get_or_create(customer=customer, complete= False)
       total = float(data['form']['total'])
       order.transaction_id = transaction_id
       if total == order.get_cart_total:
          order.complete = True
       order.save()
       if order.shipping == True:
          ShippingAddress.objects.create(
             customer=customer,
             order = order,
             address=data['form'].get('address', ''),
             state=data['form'].get('state', ''),
             zip_code=data['form'].get('zip_code', ''),
             city = data['form'].get('city', ''),
             
          )
       

       
    else:
       print('user is not logged in')
    
    return JsonResponse('payment complete', safe=False)

