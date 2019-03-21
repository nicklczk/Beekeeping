from django.shortcuts import render, redirect
import datetime

from .models import Hive
from .forms import HiveCreationForm
# Create your views here.
def viewhives(request, username):
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        try:
            hives = Hive.objects.filter(user=request.user.username)
        except Hive.DoesNotExist:
            hives = []   
        info = {
            "username": username,
            "hives": [hive for hive in hives]
        }
        
        return render(request, "viewhives.html", info)            
    
def createhive(request, username):
    if request.method == "POST":
        form = HiveCreationForm(request.POST)

        if form.is_valid():
            hive = form.save(commit=False)
            hive.user = request.user.username
            hive.creation_date = datetime.datetime.now()
            hive.save()
            return redirect("viewhives", username)
    else:
        form = HiveCreationForm()

    return render(request, "createhive.html", {"form": form})    

def viewhive(request, username, hive_pk):
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        hive = Hive.objects.get(pk=hive_pk)
        info = {
            "username": username,
            "hive_name": hive.hive_name,
            "creation_date": hive.creation_date,
            "pk": hive.pk
            }
        return render(request, "viewhive.html", info) 
    
def deletehive(request, username, hive_pk):
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        Hive.objects.filter(pk=hive_pk).delete()
        return redirect("viewhives", username)
    
def edithive(request, username, hive_pk):  
    hive = Hive.objects.get(pk=hive_pk)
    if request.method == "POST":
        form = HiveCreationForm(request.POST,initial={'hive_name':hive.hive_name})

        if form.is_valid():
            Hive.objects.filter(pk=hive_pk).delete()
            new_hive = form.save(commit=False)
            new_hive.user = request.user.username
            new_hive.creation_date = hive.creation_date
            new_hive.save()
            return redirect("viewhives", username)
    else:
        form = HiveCreationForm(initial={'hive_name':hive.hive_name})     

    return render(request, "edithive.html", {"form": form, "username": username})     
    
