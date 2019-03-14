from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy

from .forms import BeeUserCreationForm

# Create your views here.
def login(request):
    return HttpResponse("Hello, you're at the login page.")

class SignUp(generic.CreateView):

    form_class = BeeUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
