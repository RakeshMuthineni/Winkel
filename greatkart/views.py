from django.shortcuts import render
from Store.models import product

def Home(request):
    products = product.objects.all().filter(is_avilable=True)
    context = {'products':products}


    return render(request,'home.html',context)
