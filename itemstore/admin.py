from django.contrib import admin
from .models import *
from .forms import *
class StockAdmin(admin.ModelAdmin):
    list_display = ['category', 'item_name', 'quantity']
    form = StockForm
    list_filter = ['category']
    search_fields = ['category', 'item_name']
admin.site.register(Stock, StockAdmin)
admin.site.register(Category)
# Register your models here.
