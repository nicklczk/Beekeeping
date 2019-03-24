from django.shortcuts import render, redirect
import datetime
import operator
import matplotlib
matplotlib.use('Agg')
from matplotlib import pylab
import matplotlib.image as mpimg
from pylab import *
import PIL, PIL.Image

from .models import Hive, HiveTimeline
from .forms import HiveCreationForm, EntryCreationForm

def graphdata(request, username, hive_pk, data_type):
    plt.close()
    try:
        entries = HiveTimeline.objects.filter(hive_key=hive_pk)
        entries = sorted(entries, key=operator.attrgetter('timeline_date'))
    except HiveTimeline.DoesNotExist:
        entries = []   
    x = []
    y = []
    x_label=""
    if (data_type == "brood_cells"):
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.brood_cells)
            x_label = "Brood Cells"
    if (data_type == "honey_racks"):
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.honey_racks)
            x_label = "Honey Racks"    
    if (data_type == "hive_size"):
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.hive_size)
            x_label = "Hive Size"    
    if (data_type == "queen_spotted"):
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.queen_spotted)
            x_label = "Queen Spotted"    
    if (data_type == "pests_disease"):
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.pests_disease)
            x_label = "Pests/Disease"       
    if (data_type == "plant_life"):
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.plant_life)
            x_label = "Plant Life"            
    plt.plot(x,y)
    
    ylabel(x_label)
    xlabel('Time')
    title(x_label + " vs Time")
    grid(True)
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    pilImage.show()
    plt.close()
    return redirect("viewhive", username, hive_pk)


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
        try:
            entries = HiveTimeline.objects.filter(hive_key=hive_pk)
            entries = sorted(entries, key=operator.attrgetter('timeline_date'))
        except HiveTimeline.DoesNotExist:
            entries = []           
        info = {
            "username": username,
            "hive_name": hive.hive_name,
            "creation_date": hive.creation_date,
            "pk": hive.pk,
            "entries": [entry for entry in entries],
            }
        return render(request, "viewhive.html", info) 
    
def deletehive(request, username, hive_pk):
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        Hive.objects.filter(pk=hive_pk).delete()
        HiveTimeline.objects.filter(hive_key=hive_pk).delete()
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
            HiveTimeline.objects.filter(hive_key=hive_pk).update(hive_name=new_hive.hive_name)
            HiveTimeline.objects.filter(hive_key=hive_pk).update(hive_key=new_hive.pk)
            return redirect("viewhive", username, new_hive.pk)
    else:
        form = HiveCreationForm(initial={'hive_name':hive.hive_name})     

    return render(request, "edithive.html", {"form": form, "username": username, "hive_pk": hive_pk})     

def addtimelineentry(request, username, hive_pk):
    hive = Hive.objects.get(pk=hive_pk)
    if request.method == "POST":
        form = EntryCreationForm(request.POST)

        if form.is_valid():
            timeline = form.save(commit=False)
            timeline.user = request.user.username
            timeline.creation_date = datetime.datetime.now()
            timeline.edited_date = datetime.datetime.now()
            timeline.hive_name = hive.hive_name
            timeline.hive_key = hive.pk
            timeline.save()
            return redirect("viewhive", username, hive_pk)         
    else:
        form = EntryCreationForm()

    return render(request, "createevent.html", {"form": form})      

def viewtimelineentry(request, username, hive_pk, timeline_pk):
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        timeline = HiveTimeline.objects.get(pk=timeline_pk)
        try:
            entries = HiveTimeline.objects.filter(hive_key=hive_pk)
        except HiveTimeline.DoesNotExist:
            entries = []           
        info = {
            "username": username,
            "hive_name": timeline.hive_name,
            "creation_date": timeline.creation_date,
            "timeline_pk": timeline.pk,
            "hive_pk": hive_pk,
            "timeline_date": timeline.timeline_date,
            "brood_cells": timeline.brood_cells,
            "honey_racks": timeline.honey_racks,
            "hive_size": timeline.hive_size,
            "queen_spotted": timeline.queen_spotted,
            "pests_disease": timeline.pests_disease,
            "plant_life": timeline.plant_life,
            }    
        return render(request, "viewtimelineevent.html", info) 
    
def deleteevent(request, username, hive_pk, timeline_pk):
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        HiveTimeline.objects.filter(pk=timeline_pk).delete()
        return redirect("viewhive", username, hive_pk)
    
def editevent(request, username, hive_pk, timeline_pk):  
    timeline = HiveTimeline.objects.get(pk=timeline_pk)
    if request.method == "POST":
        form = EntryCreationForm(request.POST,initial={ "hive_name": timeline.hive_name,
            "creation_date": timeline.creation_date,
            "timeline_date": timeline.timeline_date,
            "brood_cells": timeline.brood_cells,
            "honey_racks": timeline.honey_racks,
            "hive_size": timeline.hive_size,
            "queen_spotted": timeline.queen_spotted,
            "pests_disease": timeline.pests_disease,
            "plant_life": timeline.plant_life,
            })

        if form.is_valid():
            HiveTimeline.objects.filter(pk=timeline_pk).delete()
            new_timeline = form.save(commit=False)
            new_timeline.user = request.user.username
            new_timeline.creation_date = timeline.creation_date
            new_timeline.edited_date = datetime.datetime.now()
            new_timeline.hive_key = timeline.hive_key
            new_timeline.hive_name = timeline.hive_name
            new_timeline.save()
            return redirect("viewtimelineentry", username, hive_pk, new_timeline.pk)
    else:
        form = EntryCreationForm(initial={"hive_name": timeline.hive_name,
            "creation_date": timeline.creation_date,
            "timeline_date": timeline.timeline_date,
            "brood_cells": timeline.brood_cells,
            "honey_racks": timeline.honey_racks,
            "hive_size": timeline.hive_size,
            "queen_spotted": timeline.queen_spotted,
            "pests_disease": timeline.pests_disease,
            "plant_life": timeline.plant_life,
            })     

    return render(request, "editevent.html", {"form": form, "username": username, "hive_pk": hive_pk, "timeline_pk": timeline_pk}) 