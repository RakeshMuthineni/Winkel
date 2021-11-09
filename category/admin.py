
from django.contrib import admin

# Register your models here.
from django.contrib.admin import site

from category.models import category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ['category_name',]



admin.site.register(category,CategoryAdmin)
