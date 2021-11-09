from django.db import models
from category.models import category
from django.urls import reverse

# Create your models here.


class product(models.Model):
    product_name = models.CharField(blank=True, max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    price = models.IntegerField(blank=True, null=True)
    images = models.ImageField(upload_to="photos/produts")
    stock = models.IntegerField(blank=True, null=True)

    is_avilable = models.BooleanField(default=True)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def get_url(self):

        return reverse('product_detail',args=[self.category.slug,self.slug])


    def __str__(self):
        return self.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

variation_category_choice = (
    ('color','color'),
    ('size','size'),
)
class Variation(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
