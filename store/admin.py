from django.contrib import admin # type: ignore
from .models import Product
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_popular', 'created_at')
    list_filter = ('is_popular',)
    search_fields = ('name',)
    