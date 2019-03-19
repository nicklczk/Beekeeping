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
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        user_info = {
            "username": request.user.username,
            "email": request.user.email,
        }

        return render(request, "profile_base.html", user_info)


def signup(request):
    if request.method == "POST":
        form = BeeUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")

    else:
        form = BeeUserCreationForm()

    return render(request, "signup.html", {"form": form})


class SignUp(generic.CreateView):

    form_class = BeeUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"
