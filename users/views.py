from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate

from .forms import BeeUserCreationForm


# Create your views here.
def login(request):
    return HttpResponse("Hello, you're at the login page.")


def profile(request, username):
    """
    profile

    Handles user profile view. Redirects user to login if the user is not
    authorized to view a profile, and if the user is it gets the necessary
    informatino and renders the proper template
    """
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        user_info = {
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "zipcode": request.user.zipcode,
        }

        return render(request, "profile_base.html", user_info)


def signup(request):
    """
    signup

    Handles account registration through Django built in
    user auth
    """
    if request.method == "POST":
        # Double check the form was actually submitted, instead of the page being
        # loaded
        form = BeeUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")

    else:
        # If the page was just loaded, set the form to the proper one
        form = BeeUserCreationForm()

    return render(request, "signup.html", {"form": form})


class SignUp(generic.CreateView):

    form_class = BeeUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"
