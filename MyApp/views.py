from datetime import date as date_type

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import Car, Contact, Order


def index(request):
    featured_cars = Car.objects.all()[:6]
    return render(request, "index.html", {"featured_cars": featured_cars})


def about(request):
    return render(request, "about.html")


def register(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        if not all([name, username, email, password, password2]):
            messages.error(request, "Please fill in all required fields.")
            return redirect("register")
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "That username is already taken.")
            return redirect("register")
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with that email already exists.")
            return redirect("register")
        if len(password) < 8:
            messages.error(request, "Password must contain at least 8 characters.")
            return redirect("register")
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name,
        )
        messages.success(request, "Account created successfully. You can now sign in.")
        return redirect("signin")

    return render(request, "register.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("loginusername", "").strip()
        password = request.POST.get("loginpassword", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}.")
            return redirect("vehicles")

        messages.error(request, "Invalid username or password.")
        return redirect("signin")

    return render(request, "login.html")


def signout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


@login_required
def vehicles(request):
    cars = Car.objects.all()
    return render(request, "vehicles.html", {"car": cars})


@login_required
def bill(request):
    cars = Car.objects.all()
    selected_car = request.GET.get("car", "")
    return render(request, "bill.html", {"cars": cars, "selected_car": selected_car})


@login_required
def order(request):
    if request.method != "POST":
        return redirect("bill")

    data = {
        "name": request.POST.get("billname", "").strip(),
        "email": request.POST.get("billemail", "").strip().lower(),
        "phone": request.POST.get("billphone", "").strip(),
        "address": request.POST.get("billaddress", "").strip(),
        "city": request.POST.get("billcity", "").strip(),
        "state": request.POST.get("state", "").strip(),
        "pincode": request.POST.get("pincode", "").strip(),
        "cars": request.POST.get("cars11", "").strip(),
        "car_color": request.POST.get("color1", "").strip(),
        "days": request.POST.get("dayss", "").strip(),
        "date": request.POST.get("date", "").strip(),
        "loc_from": request.POST.get("fl", "").strip(),
        "loc_to": request.POST.get("tl", "").strip(),
    }

    required = [data[key] for key in ("name", "email", "phone", "address", "city", "cars", "days", "date", "loc_from", "loc_to")]
    if not all(required):
        messages.error(request, "Please complete all required booking fields.")
        return redirect("bill")

    try:
        days = int(data["days"])
    except ValueError:
        days = 0

    if days < 1 or days > 30:
        messages.error(request, "Rental duration must be between 1 and 30 days.")
        return redirect("bill")

    try:
        pickup_date = date_type.fromisoformat(data["date"])
    except ValueError:
        messages.error(request, "Please choose a valid pickup date.")
        return redirect("bill")

    if pickup_date < date_type.today():
        messages.error(request, "Pickup date cannot be in the past.")
        return redirect("bill")

    car = get_object_or_404(Car, car_name=data["cars"])
    total_rent = car.price * days

    booking = Order.objects.create(
        user=request.user,
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        address=data["address"],
        city=data["city"],
        state=data["state"],
        pincode=data["pincode"],
        cars=car.car_name,
        car_color=data["car_color"],
        days_for_rent=days,
        date=data["date"],
        loc_from=data["loc_from"],
        loc_to=data["loc_to"],
        total_rent=total_rent,
    )

    messages.success(request, f"Booking #{booking.order_id} confirmed. Total: ₹{total_rent:,}.")
    return redirect("my_bookings")


@login_required
def my_bookings(request):
    bookings = Order.objects.filter(user=request.user)
    return render(request, "my_bookings.html", {"bookings": bookings})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("contactname", "").strip()
        email = request.POST.get("contactemail", "").strip().lower()
        phone = request.POST.get("contactnumber", "").strip()
        message_text = request.POST.get("contactmsg", "").strip()

        if not all([name, email, phone, message_text]):
            messages.error(request, "Please complete every contact field.")
            return redirect("contact")

        Contact.objects.create(
            name=name,
            email=email,
            phone_number=phone,
            message_text=message_text,
        )
        messages.success(request, "Thanks. Your message has been received.")
        return redirect("contact")

    return render(request, "contact.html")
