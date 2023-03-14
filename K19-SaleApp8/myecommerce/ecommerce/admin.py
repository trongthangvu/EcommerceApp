from django.contrib import admin
from .models import Product, Category, Cart, CartItem, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'image', 'created_at', 'updated_at', 'category')
    list_display_links = ('id', 'name')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    list_per_page = 25

    def delete_model(self, request, obj):
        obj.delete()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fields = ['name', 'description', 'price', 'image', 'category']
        return super().change_view(request, object_id, form_url='', extra_context=None)

    def add_view(self, request, form_url='', extra_context=None):
        self.fields = ['name', 'description', 'price', 'image', 'category']
        return super().add_view(request, form_url='', extra_context=None)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_per_page = 25


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    list_display_links = ('id', 'user')
    search_fields = ('user',)
    list_per_page = 25


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    list_display_links = ('id', 'cart')
    list_filter = ('cart',)
    search_fields = ('product__name', 'cart__user__username')
    list_per_page = 25


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    list_display_links = ('id', 'user')
    search_fields = ('user',)
    list_per_page = 25


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
