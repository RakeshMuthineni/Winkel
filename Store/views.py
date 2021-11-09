from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.shortcuts import render,get_object_or_404
from category.models import category
from Store.models import product
from carts.models import CartItem
from carts.views import _cart_id
from django.db.models import Q

# Create your views here.
def store(request,category_slug=None):
    products = None
    categories = None

    if category_slug != None:
        categories = get_object_or_404(category,slug=category_slug)
        products = product.objects.all().filter(category = categories,is_avilable=True)
        paginator = Paginator(products,5)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:

        products = product.objects.all().filter(is_avilable=True).order_by('id')
        paginator = Paginator(products,5)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()


    context = {
    'products':paged_products,
    'product_count':product_count,
    }

    return render(request,'store/store.html',context)





def product_detail(request,category_slug,product_slug):
    try:
        single_product = product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()

    except Exception as e:
        raise e

    context = {
        'single_product' : single_product,
        'in_cart':in_cart,

    }
    return render(request,'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

            context={
                'products':products,
                'product_count': product_count,
                'keyword':keyword,
            }

    return render(request,'store/store.html',context)
