from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from . models import *

# these are function based views
# Create your views here.
def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # we are either going to create or find a customer
        items = order.orderitem_set.all()
        # quering out the item prop that we created in models
        cartItems = order.get_cart_items
    else:
        # this will make sure that even users who are not logged
        # in will get their data rendered out 
        items = []
        order = {
            'get_cart_table':0, 'get_cart_items':0, 'shipping': False
        }
        cartItems = order['get_cart_items']

    products = Product.objects.all()
   
    context = {
        'products':products, 
        'first_row':products[:4],
        'sec_row':products[4:8],
        'thrid_row':products[8:12],
        'cartItems': cartItems,
        }
    # context dict because we will be passing data
    return render(request, 'store/store.html', context)

def cart(request):
    # will check both authenticated and 
    # not logged in users before adding items in cart
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # we are either going to create or find a customer
        items = order.orderitem_set.all()
        # quering out the item prop that we created in models
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_table':0, 'get_cart_items':0, 'shipping': False
        }
        cartItems = order['get_cart_items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout (request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # we are either going to create or find a customer
        items = order.orderitem_set.all()
        # quering out the item prop that we created in models
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_table':0, 'get_cart_items':0, 'shipping': False 
        }
        cartItems = order['get_cart_items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def products(request):
    products = Product.objects.all()
   
    context = {
        'products':products, 
        'first_row':products[:4],
        'sec_row':products[4:8],
        'thrid_row':products[8:12],
      
        }
    
    return render(request, 'store/products.html', context)

def about(request):
    context = {}
    return render(request, 'store/about.html', context)


def updateItem(request):
    data = json.loads(request.body)
    # return JsonResponse('Item was added', safe=False)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

# this wil be functionalty for the cart
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
# this will help us delete items complety from the cart

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    # print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_table):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],


            )
    else:
        print('user is not logged in ..')
    return JsonResponse('Payment complete', safe=False)