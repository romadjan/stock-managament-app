from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponse
import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    title = "HomePage"
    h1 = "Welcome to our Homepage"
    context = {
        "title": title,
        "h1": h1
    }
    return render(request, "itemstore/home.html", context)


@login_required
def list_item(request):
    title = 'List of Items'
    items = Stock.objects.all()
    h1 = "List of items"
    form = StockSearchForm(request.POST or None)
    context = {
        "title": title,
        "items": items,
        "form": form,
        "h1": h1
    }
    if request.method == 'POST':
        category = form['category'].value()
        items = StockHistory.objects.filter(
            item_name__icontains=form['item_name'].value()
        )

        if (category != ''):
            items = items.filter(category_id=category)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = items
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
        context = {
            "form": form,
            "title": title,
            "items": items,
            "h1": h1
        }
    return render(request, "itemstore/list_item.html", context)


@login_required
def add_item(request):
    form = StockForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Item add successfully')
        return redirect("/list_item")

    context = {
        "form": form,
        "title": "Add Item",
        "h1": "Add Item"
    }
    return render(request, "itemstore/add_item.html", context)


def update_item(request, pk):
    items = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=items)
    if request.method == "POST":
        form = StockUpdateForm(request.POST, instance=items)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item update successfully')
            return redirect("/list_item")
    context = {
        "form": form,
        "title": "Update Item",
        "h1": "Update Item"
    }
    return render(request, "itemstore/add_item.html", context)


def delete_item(request, pk):
    items = Stock.objects.get(id=pk)
    if request.method == "POST":
        items.delete()
        messages.success(request, 'Item delete successfully')
        return redirect("/list_item")
    return render(request, "itemstore/delete_item.html")


def item_detail(request, pk):
    items = Stock.objects.get(id=pk)
    context = {
        "title": items.item_name,
        "items": items,
        "h1": "Item Detail"
    }
    return render(request, "itemstore/item_detail.html", context)

def issue_items(request, pk):
    items = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=items)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.issue_by = str(request.user)
        instance.quantity -= instance.issue_quantity
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        instance.save()

        return redirect('/item_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(items.item_name),
        "items": items,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "itemstore/add_item.html", context)


def receive_items(request, pk):
    items = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=items)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.receive_by = str(request.user)
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

        return redirect('/item_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
            "title": 'Receive ' + str(items.item_name),
            "items": items,
            "form": form,
            "username": 'Receive By: ' + str(request.user),
        }
    return render(request, "itemstore/add_item.html", context)


def reorder_level(request, pk):
    items = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=items)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

        return redirect("/list_item")
    context = {
            "items": items,
            "form": form,
        }
    return render(request, "itemstore/add_item.html", context)


@login_required
def list_history(request):
    h1 = 'HISTORY DATA'
    items = StockHistory.objects.all()
    form = StockHistorySearchForm(request.POST or None)
    context = {
        "h1": h1,
        "items": items,
        "form": form
    }
    if request.method == 'POST':
        category = form['category'].value()
        items = StockHistory.objects.filter(
            item_name__icontains=form['item_name'].value(),
            last_updated__range=[
                form['start_date'].value(),
                form['end_date'].value()
            ]
        )

        if (category != ''):
            items = items.filter(category_id=category)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(
                ['CATEGORY',
                 'ITEM NAME',
                 'QUANTITY',
                 'ISSUE QUANTITY',
                 'RECEIVE QUANTITY',
                 'RECEIVE BY',
                 'ISSUE BY',
                 'LAST UPDATED'])
            instance = items
            for stock in instance:
                writer.writerow(
                    [stock.category,
                     stock.item_name,
                     stock.quantity,
                     stock.issue_quantity,
                     stock.receive_quantity,
                     stock.receive_by,
                     stock.issue_by,
                     stock.last_updated])
            return response

        context = {
            "form": form,
            "h1": h1,
            "items": items,
        }
    return render(request, "itemstore/list_history.html", context)

# Create your views here.
