from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate,
                                 login,
                                 logout)
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock
from .forms import StockForm


import requests
import json

# Create your views here.


def home(request):

    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get(
            "https://cloud.iexapis.com/v1/stock/" + ticker + "/quote?token=")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})


def about(request):
    return render(request, 'about.html', {})

# ________________________________________________
def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_passwd)
            if user is not None:
                login(request, user)
            else:
                return redirect('login')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
# ________________________________________________


@login_required
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            # form.save()
            stock = form.save(commit=False)
            stock.user = request.user
            stock.save()
            messages.success(request, "Stock Has Been Added!")
            return redirect('add_stock')

    else:
        # ticker = Stock.objects.all()
        ticker = Stock.objects.filter(user=request.user)  # założyc filter po Userach
        output = []

        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/v1/stock/" + str(ticker_item) + "/quote?token=")

            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                e.api = "Error..."

        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

@login_required
def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id, user=request.user)  # sprawdzić zabazpieczenie czy delete tylko dla zalogowanej osoby
    item.delete()
    messages.success(request, "Stock has been Deleted!")
    return redirect(delete_stock)

@login_required
def delete_stock(request):
    ticker = Stock.objects.filter(user=request.user)
    return render(request, 'delete_stock.html', {'ticker': ticker})

