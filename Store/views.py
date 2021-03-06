from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.shortcuts import render, get_object_or_404, redirect
from category.models import category
from Store.models import product,ReviewRating,ProductGallery
from carts.models import CartItem
from carts.views import _cart_id
from django.db.models import Q
from django.contrib import messages
from .forms import ReviewRatingForm
from orders.models import OrderProduct


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
    if request.user.is_authenticated:
        try:
            orderproduct= OrderProduct.objects.filter(user=request.user,product=single_product).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the  REVIEW:

    reviews = ReviewRating.objects.filter(product_id=single_product.id,status=True)

    # Get the product Gallary

    product_gallery = ProductGallery.objects.filter(product_id = single_product.id)


    context = {
        'single_product' : single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'product_gallery':product_gallery,

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


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewRatingForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
