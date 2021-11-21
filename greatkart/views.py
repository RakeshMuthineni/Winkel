from django.shortcuts import render
from Store.models import product

def home(request):
    products = product.objects.all().filter(is_avilable=True).order_by('-created_date')
    context = {'products':products}


    return render(request,'home.html',context)
