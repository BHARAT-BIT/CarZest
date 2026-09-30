from django.contrib import admin

from .models import Car, Contact, Order


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("car_id", "car_name", "price")
    search_fields = ("car_name", "car_desc")
    list_filter = ("price",)
    ordering = ("car_id",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "name", "user", "cars", "days_for_rent", "total_rent", "status", "date")
    search_fields = ("name", "email", "cars", "phone")
    list_filter = ("status", "cars", "date")
    readonly_fields = ("created_at", "total_rent")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number", "created_at")
    search_fields = ("name", "email", "message_text")
    readonly_fields = ("created_at",)
