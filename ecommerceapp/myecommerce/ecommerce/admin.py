from django.contrib import admin
from .models import User, Profile, Store, Product, Review, Order, OrderItem, ShippingAddress, Payment


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    fieldsets = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'store')
    list_filter = ('store',)
    search_fields = ('name', 'description')
    ordering = ('-id',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'comment')
    list_filter = ('product', 'rating')
    search_fields = ('user__username', 'product__name')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_ordered', 'complete')
    list_filter = ('complete',)
    search_fields = ('user__username',)
    ordering = ('-id',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added')
    list_filter = ('product', 'order')
    search_fields = ('product__name',)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'address', 'city', 'state', 'zipcode', 'date_added')
    list_filter = ('user', 'order')
    search_fields = ('user__username', 'order__id', 'address', 'city', 'state', 'zipcode')
    ordering = ('-id',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'payment_method', 'date_paid', 'transaction_id', 'amount')
    list_filter = ('user', 'order', 'payment_method')
    search_fields = ('user__username', 'order__id', 'transaction_id')
    ordering = ('-id',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Payment, PaymentAdmin)
