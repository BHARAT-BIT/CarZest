from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Car, Order


class CarZestBookingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="demo_user",
            email="demo@example.com",
            password="strong-password-123",
            first_name="Demo User",
        )
        self.car = Car.objects.create(
            car_id=1,
            car_name="Test Car",
            car_desc="A test vehicle",
            price=1500,
            image="car/images/test.jpg",
        )

    def test_vehicle_page_requires_login(self):
        response = self.client.get(reverse("vehicles"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("signin"), response.url)

    def test_authenticated_user_can_view_vehicles(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("vehicles"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Car")

    def test_booking_total_is_calculated_server_side(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("order"), {
            "billname": "Demo User",
            "billemail": "demo@example.com",
            "billphone": "9876543210",
            "billaddress": "123 Main Street",
            "billcity": "Meerut",
            "state": "Uttar Pradesh",
            "pincode": "250001",
            "cars11": "Test Car",
            "color1": "Black",
            "dayss": "3",
            "date": (date.today() + timedelta(days=2)).isoformat(),
            "fl": "Meerut",
            "tl": "Delhi",
        })
        self.assertRedirects(response, reverse("my_bookings"))
        booking = Order.objects.get(user=self.user)
        self.assertEqual(booking.total_rent, 4500)
        self.assertEqual(booking.days_for_rent, 3)

    def test_user_only_sees_own_bookings(self):
        other_user = User.objects.create_user(username="other", password="strong-password-123")
        Order.objects.create(user=other_user, name="Other", cars="Test Car", days_for_rent=1, total_rent=1500)
        self.client.force_login(self.user)
        response = self.client.get(reverse("my_bookings"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Other")
