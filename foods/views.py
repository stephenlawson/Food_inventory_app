
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import FoodItemForm, FoodItemFormAPI, FoodItemFormArc, FoodItemFormManual
from .filters import FoodFilter
from django.db.models import Count
from datetime import date
import requests


def test_api_cite(barcode):
    """upc barcode lookup API"""
    url_cite = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
    response_cite = requests.get(url_cite, verify=False)
    data_cite = response_cite.json()
    api_response_cite = data_cite['total']
    return api_response_cite

def test_api_nut(barcode):
    """upc barcode lookup API (also finds good nutrition information, try to implement later)"""
    appId = "b634f50d"
    appKey = "5a3df06b4f25314c2a1d67abc9674308"
    url_nut = f'https://api.nutritionix.com/v1_1/item?upc={barcode}&appId={appId}&appKey={appKey}'
    response_nut = requests.get(url_nut, verify=False)
    data_nut = response_nut.json()
    api_response_nut = data_nut['status_code']
    return api_response_nut

@login_required
def dashboard(request):
    """User dashboard with custom information depending on food catalogue"""
    user = request.user
    foods = Foods.objects.filter(author=user).order_by('Days_Left')
    foods_expired = Foods.objects.filter(author=user).filter(Days_Left__lte=0).count()
    total = Foods.objects.filter(author=user).count()
    sorted_user = Foods.objects.filter(author=user)
    if foods:
        most_common = sorted_user.values("product_name").annotate(mc=Count('product_name')).order_by('-mc')[0]['product_name']
    else:
        most_common = "None"
    myFilter = FoodFilter(request.GET, queryset=foods)
    foods = myFilter.qs
    context = {'foods':foods, 'myFilter':myFilter, 'foods_expired':foods_expired, 'total': total, 'most_common':most_common}
    return render(request, 'foods/dashboard.html', context)

def SearchArchive(request):
    """queries a separte database for information saved initially from manual/api insertion"""
    if request.method == "POST":
        searched = request.POST.get('searched', False)
        if request.method == 'POST':
                foods = Foods_archive.objects.filter(barcode__contains=searched).first()
                if foods is None:
                    try:
                        api_value1 = test_api_cite(searched)
                    except:
                        return redirect(f'/foods/manual_form/{searched}/')
                    try:
                        api_value2 = test_api_nut(searched)
                    except:
                        return redirect(f'/foods/API_form/{searched}/')
                    if api_value1 == 0:
                        return redirect(f'/foods/manual_form/{searched}/')
                    if api_value2 == '404':
                        return redirect(f'/foods/manual_form/{searched}/')
                    if api_value2 == '400':
                            return redirect(f'/foods/manual_form/{searched}/')
                else:
                    barcode = foods.barcode
                    return redirect(f'/foods/archive_form/{searched}/')
        return render(request, 'foods/dashboard.html', {'searched': searched})
    else:
        return render(request, 'foods/dashboard.html', {})

def ArchiveForm(request, barcode): 
    """form served if most most information is already found in database"""
    food = Foods_archive.objects.get(barcode=barcode)
    product_name = food.product_name 
    category = food.category
    sub_category = food.sub_category
    location = food.location
    form = FoodItemFormArc
    if request.method == 'POST':
        form = FoodItemFormArc(request.POST)
        if form.is_valid():
            date_start = date.today()
            date_end = form.cleaned_data.get('expiration')
            form.instance.barcode = barcode
            form.instance.product_name = product_name
            form.instance.category = category
            form.instance.sub_category = sub_category
            form.instance.location = location
            form.instance.author = request.user
            time_delta = date_end - date_start
            form.instance.Days_Left= int(str(time_delta.days))
            form.instance.author = request.user
            form.save()
            return redirect('/foods/')
    context = {'form':form, 'barcode':barcode, 'product_name': product_name,
    'category':category, 'sub_category': sub_category, 'location': location}
    return render (request, 'foods/archive_form.html', context)

def APIForm(request, barcode):
    """form served if API can find barcode"""
    url_cite = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
    response_cite = requests.get(url_cite, verify=False)
    data_cite = response_cite.json()
    appId = "b634f50d"
    appKey = "5a3df06b4f25314c2a1d67abc9674308"
    url_nut = f'https://api.nutritionix.com/v1_1/item?upc={barcode}&appId={appId}&appKey={appKey}'
    response_nut = requests.get(url_nut, verify=False)
    data_nut = response_nut.json()
    product_name = data_nut['brand_name'] + ' ' + data_nut['item_name']
    cat_full = data_cite['items'][0]['category']
    split_cat = cat_full.split('>')
    category = split_cat[-2].strip()
    sub_category = split_cat[-1].strip()
    form = FoodItemFormAPI
    if request.method == 'POST':
        form = FoodItemFormAPI(request.POST)
        if form.is_valid():
            date_start = date.today()
            date_end = form.cleaned_data.get('expiration')
            form.instance.barcode = barcode
            form.instance.product_name = product_name
            form.instance.category = category
            form.instance.sub_category = sub_category
            form.instance.author = request.user
            time_delta = date_end - date_start
            form.instance.Days_Left= int(str(time_delta.days))
            form.instance.author = request.user
            Foods_a = Foods_archive(barcode=form.instance.barcode,
                                    product_name = form.instance.product_name,
                                    category = form.instance.category,
                                    sub_category = form.instance.sub_category,
                                    location = form.instance.location
            )
            Foods_a.save()
            form.save()
            return redirect('/foods/')
    context = {'form':form, 'barcode':barcode, 'product_name': product_name,
    'category':category, 'sub_category': sub_category}
    return render (request, 'foods/API_form.html', context)

def ManualForm(request, barcode):
    """form served when api/database cannot find barcode and manual addition is needed"""
    form = FoodItemFormManual()
    if request.method == 'POST':
        form = FoodItemFormManual(request.POST)
        if form.is_valid():
            date_start = date.today()
            date_end = form.cleaned_data.get('expiration')
            form.instance.barcode = barcode
            form.instance.author = request.user
            time_delta = date_end - date_start
            form.instance.Days_Left= int(str(time_delta.days))
            form.instance.author = request.user
            form.save()
            Foods_a = Foods_archive(barcode=form.instance.barcode,
                                    product_name = form.instance.product_name,
                                    category = form.instance.category,
                                    sub_category = form.instance.sub_category,
                                    location = form.instance.location
            )
            Foods_a.save()
            return redirect('/foods/')
    context = {'form':form, 'barcode':barcode}
    return render (request, 'foods/manual_form.html', context)


def CreateFoodItem(request):
    """Like manual creation but presents an empty barcode field"""
    form = FoodItemForm
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            date_start = date.today()
            date_end = form.cleaned_data.get('expiration')
            form.instance.author = request.user
            time_delta = date_end - date_start
            form.instance.Days_Left= int(str(time_delta.days))
            Foods_a = Foods_archive(barcode=form.instance.barcode,
                                    product_name = form.instance.product_name,
                                    category = form.instance.category,
                                    sub_category = form.instance.sub_category,
                                    location = form.instance.location
            )
            Foods_a.save()
            form.save()
            return redirect('/foods/')
    context = {'form':form}
    return render (request, 'foods/create_food_item.html', context)

def UpdateFoodItem(request, pk):
    """Update items aready in database"""
    food = Foods.objects.get(id=pk)
    form = FoodItemForm(instance=food)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=food)
        if form.is_valid():
            date_start = date.today()
            date_end = form.cleaned_data.get('expiration')
            form.instance.author = request.user
            time_delta = date_end - date_start
            form.instance.Days_Left= int(str(time_delta.days))
            form.instance.author = request.user
            form.save()
            return redirect('/foods/')
    context = {'form':form}
    return render (request, 'foods/create_food_item.html', context)

def DeleteFoodItem(request, pk):
    food = Foods.objects.get(id=pk)
    if request.method == "POST":
        food.delete()
        return redirect('/foods/')
    context = {'item':food}
    return render(request, 'foods/delete.html', context)