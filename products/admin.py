from django.contrib import admin

from .models import Plan, Customer


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'Name',
        'plan_id',
        'Description',
        'Price',
        'Image',
        'stripe_price_id',
        'isDelete',
    )
    list_filter = ('isDelete',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'stripe_id',
        'stripe_subscription_id',
        'plan',
        'payment_method',
        'buy_at',
        'deadline',
        'address',
        'has_active_plan',
    )
    list_filter = (
        'customer',
        'plan',
        'buy_at',
        'deadline',
        'has_active_plan',
    )