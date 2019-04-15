from django.shortcuts import render, redirect
import datetime
import operator
import matplotlib

matplotlib.use("Agg")
from matplotlib import pylab
import matplotlib.image as mpimg
from pylab import *
import PIL, PIL.Image
import csv
from django.http import HttpResponse
from .models import Hive, HiveTimeline
from .forms import HiveCreationForm, EntryCreationForm

# Creates a graph from the data associated with a hive
def graphdata(request, username, hive_pk, data_type):
    plt.close()

    # Get the entries for the hive
    try:
        entries = HiveTimeline.objects.filter(hive_key=hive_pk)
        entries = sorted(entries, key=operator.attrgetter("timeline_date"))
    except HiveTimeline.DoesNotExist:
        entries = []
    x = []
    y = []
    x_label = ""

    # Get the specific data depending on what type of graph is requested
    if data_type == "brood_cells":
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.brood_cells)
            x_label = "Brood Cells"
    elif data_type == "honey_racks":
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.honey_racks)
            x_label = "Honey Racks"
    elif data_type == "hive_size":
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.hive_size)
            x_label = "Hive Size"
    elif data_type == "queen_spotted":
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.queen_spotted)
            x_label = "Queen Spotted"
    elif data_type == "pests_disease":
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.pests_disease)
            x_label = "Pests/Disease"
    elif data_type == "plant_life":
        for entry in entries:
            x.append(entry.timeline_date)
            y.append(entry.plant_life)
            x_label = "Plant Life"

    # Create a graph using the data and display it
    plt.plot(x, y)
    ylabel(x_label)
    xlabel("Time")
    title(x_label + " vs Time")
    grid(True)
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    pilImage = PIL.Image.frombytes(
        "RGB", canvas.get_width_height(), canvas.tostring_rgb()
    )
    pilImage.show()
    plt.close()
    return redirect("viewhive", username, hive_pk)


# Shows all of the user's hives to the user
def viewhives(request, username):
    # Redirect the user to the login if the user is not logged in
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:

        # Get all hives associated with the user and display them
        try:
            hives = Hive.objects.filter(user=request.user.username)
        except Hive.DoesNotExist:
            hives = []
        info = {"username": username, "hives": [hive for hive in hives]}

        return render(request, "viewhives.html", info)


# Create a new hive for the user
def createhive(request, username):
    if request.method == "POST":
        form = HiveCreationForm(request.POST)

        # Get the data from the form and create a new hive from that data
        if form.is_valid():
            hive = form.save(commit=False)
            hive.user = request.user.username
            hive.creation_date = datetime.datetime.now()
            hive.save()
            return redirect("viewhives", username)
    else:
        form = HiveCreationForm()

    return render(request, "createhive.html", {"form": form})


# View the details of a specific hive
def viewhive(request, username, hive_pk):
    # Redirect the user to the login if the user is not logged in
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        # Get the hive from the database
        hive = Hive.objects.get(pk=hive_pk)
        try:
            entries = HiveTimeline.objects.filter(hive_key=hive_pk)
            entries = sorted(entries, key=operator.attrgetter("timeline_date"))
        except HiveTimeline.DoesNotExist:
            entries = []

        # Display the information on the hive
        info = {
            "username": username,
            "hive_name": hive.hive_name,
            "creation_date": hive.creation_date,
            "pk": hive.pk,
            "entries": [entry for entry in entries],
        }
        return render(request, "viewhive.html", info)


# Deletes a selected hive
def deletehive(request, username, hive_pk):
    # Redirect the user to the login if the user is not logged in
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        # Delete the hive from the database
        Hive.objects.filter(pk=hive_pk).delete()
        HiveTimeline.objects.filter(hive_key=hive_pk).delete()
        return redirect("viewhives", username)


# Edit the information saved for a hive
def edithive(request, username, hive_pk):
    hive = Hive.objects.get(pk=hive_pk)
    if request.method == "POST":
        form = HiveCreationForm(request.POST, initial={"hive_name": hive.hive_name})

        # Update the hive with the new information
        if form.is_valid():
            Hive.objects.filter(pk=hive_pk).delete()
            new_hive = form.save(commit=False)
            new_hive.user = request.user.username
            new_hive.creation_date = hive.creation_date
            new_hive.save()
            HiveTimeline.objects.filter(hive_key=hive_pk).update(
                hive_name=new_hive.hive_name
            )
            HiveTimeline.objects.filter(hive_key=hive_pk).update(hive_key=new_hive.pk)
            return redirect("viewhive", username, new_hive.pk)
    else:
        form = HiveCreationForm(initial={"hive_name": hive.hive_name})

    return render(
        request,
        "edithive.html",
        {"form": form, "username": username, "hive_pk": hive_pk},
    )


# Create a new event on the timeline for a hive
def addtimelineentry(request, username, hive_pk):
    hive = Hive.objects.get(pk=hive_pk)
    if request.method == "POST":
        form = EntryCreationForm(request.POST)

        # Create the event for the hive and add it to the database
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


# View a timeline event for a selected hive
def viewtimelineentry(request, username, hive_pk, timeline_pk):

    # Redirect the user to the login if the user is not logged in
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        # Get the timeline from the database
        timeline = HiveTimeline.objects.get(pk=timeline_pk)
        try:
            entries = HiveTimeline.objects.filter(hive_key=hive_pk)
        except HiveTimeline.DoesNotExist:
            entries = []

        # Display the information to the user
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


# Deletes a timeline event for a hive
def deleteevent(request, username, hive_pk, timeline_pk):
    # Redirect the user to the login if the user is not logged in
    if not request.user.is_authenticated:
        print("ERROR: not authenticated")
        return redirect("login")
    else:
        # Delete the event from the database
        HiveTimeline.objects.filter(pk=timeline_pk).delete()
        return redirect("viewhive", username, hive_pk)


# Edit a timeline event for a hvie
def editevent(request, username, hive_pk, timeline_pk):
    timeline = HiveTimeline.objects.get(pk=timeline_pk)
    if request.method == "POST":

        # Create a form with the initial entries as the original data
        form = EntryCreationForm(
            request.POST,
            initial={
                "hive_name": timeline.hive_name,
                "creation_date": timeline.creation_date,
                "timeline_date": timeline.timeline_date,
                "brood_cells": timeline.brood_cells,
                "honey_racks": timeline.honey_racks,
                "hive_size": timeline.hive_size,
                "queen_spotted": timeline.queen_spotted,
                "pests_disease": timeline.pests_disease,
                "plant_life": timeline.plant_life,
            },
        )

        # Update the event with the new information supplied from the user
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
        # Create a form with the initial entries as the original data
        form = EntryCreationForm(
            initial={
                "hive_name": timeline.hive_name,
                "creation_date": timeline.creation_date,
                "timeline_date": timeline.timeline_date,
                "brood_cells": timeline.brood_cells,
                "honey_racks": timeline.honey_racks,
                "hive_size": timeline.hive_size,
                "queen_spotted": timeline.queen_spotted,
                "pests_disease": timeline.pests_disease,
                "plant_life": timeline.plant_life,
            }
        )

    return render(
        request,
        "editevent.html",
        {
            "form": form,
            "username": username,
            "hive_pk": hive_pk,
            "timeline_pk": timeline_pk,
        },
    )

# Adds a hive to a csv file
def createhivecsvresponse(request, username, hive_pk, response):
    hive = Hive.objects.get(pk=hive_pk)
    response["Content-Disposition"] = (
        'attachment; filename="' + hive.hive_name + '".csv"'
    )
    writer = csv.writer(response)
    
    # Add the hive information and the information for all of the events associated with this hive
    writer.writerow([hive.hive_name, hive.user, hive.creation_date])
    try:
        entries = HiveTimeline.objects.filter(hive_key=hive_pk)
        entries = sorted(entries, key=operator.attrgetter("timeline_date"))
    except HiveTimeline.DoesNotExist:
        entries = []

    for entry in entries:
        writer.writerow(
            [
                entry.timeline_date,
                entry.brood_cells,
                entry.honey_racks,
                entry.hive_size,
                entry.queen_spotted,
                entry.pests_disease,
                entry.plant_life,
            ]
        )
    writer.writerow([])
    return response

# Creates a csv file for a given hive
def createhivecsv(request, username, hive_pk):
    response = HttpResponse(content_type="text/csv")
    return createhivecsvresponse(request, username, hive_pk, response)

# Creates a csv file for all hives for a user
def createhivescsv(request, username):
    response = HttpResponse(content_type="text/csv")
    
    # Get all hives and add each of them to the csv
    try:
        hives = Hive.objects.filter(user=request.user.username)
    except Hive.DoesNotExist:
        hives = []
    for hive in hives:
        createhivecsvresponse(request, username, hive.pk, response)
    response["Content-Disposition"] = 'attachment; filename="hives".csv"'
    return response
