from django.contrib import admin

# Register your models here.
from shop.models import Item, User

admin.site.register(Item)
admin.site.register(User)
