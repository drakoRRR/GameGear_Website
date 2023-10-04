from django.contrib import admin

from orders.models import Order


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'initiator', 'email', 'first_name', 'last_name', 'status')
    fields = ('id', 'created',
              ('first_name', 'last_name'),
              ('email', 'address'),
              'basket_history', 'status', 'initiator',
              )
    readonly_fields = ('id', 'created')
