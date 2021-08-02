from django.shortcuts import render

def store(request):
    context = {}
    return render(request, 'store/store.html', context)

def about(request):
    context = {}
    return render(request, 'store/about.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

    
def products(request):
    context = {}
    return render(request, 'store/products.html', context)

