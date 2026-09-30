from django.contrib.auth.models import User
from django.db import models


class Car(models.Model):
    car_id = models.IntegerField(unique=True, default=0)
    car_name = models.CharField(max_length=30, default="")
    car_desc = models.CharField(max_length=300, default="")
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="uploads/cars", default="")

    class Meta:
        ordering = ["car_id"]

    def __str__(self):
        return self.car_name

    @property
    def image_source(self):
        """Return the media URL when an upload exists, otherwise use a static fallback."""
        if self.image and self.image.name:
            return self.image.url
        return ""


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    name = models.CharField(max_length=90, default="")
    email = models.EmailField(max_length=150, default="")
    phone = models.CharField(max_length=20, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="", blank=True)
    pincode = models.CharField(max_length=10, default="", blank=True)
    cars = models.CharField(max_length=50, default="")
    car_color = models.CharField(max_length=20, default="", blank=True)
    days_for_rent = models.PositiveIntegerField(default=0)
    date = models.CharField(max_length=50, default="")
    loc_from = models.CharField(max_length=50, default="")
    loc_to = models.CharField(max_length=50, default="")
    total_rent = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="Confirmed")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.order_id} - {self.name} - {self.cars}"


class Contact(models.Model):
    name = models.CharField(max_length=150, default="")
    email = models.EmailField(max_length=150, default="")
    phone_number = models.CharField(max_length=15, default="")
    message_text = models.TextField(max_length=500, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
