from django.shortcuts import render, redirect
from .models import *
from .forms import *


def home(request):
    title = "HomePage"
    h1 = "Welcome to our Homepage"
    context = {
        "title": title,
        "h1": h1
    }
    return render(request, "itemstore/home.html", context)


def list_item(request):
    title = 'List of Items'
    items = Stock.objects.all()
    h1 = "List of items"

    context = {
        "title": title,
        "items": items,
        "h1": h1
    }
    return render(request, "itemstore/list_item.html", context)


def add_item(request):
    form = StockForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("/list_item")

    context = {
        "form": form,
        "title": "Add Item",
        "h1": "Add Item"
    }
    return render(request, "itemstore/add_item.html", context)
