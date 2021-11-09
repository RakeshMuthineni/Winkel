from django.db import models
from django.urls import reverse

# Create your models here.

##categories

class category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.CharField(max_length=80, blank=True)
    cat_image = models.ImageField(upload_to="photos/categories", blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):

        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name

    
