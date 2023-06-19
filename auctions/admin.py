from django.contrib import admin
from .models import User, Category, Listings, Comment, Bid
# Register your models here.
class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "description", "listing_creator", "img", "active", "category")

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listings)
admin.site.register(Comment)
admin.site.register(Bid)