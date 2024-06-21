from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import InventoryModel
from .forms import InventoryForm
# Create your views here.


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            request.session.set_expiry(86400)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

        else:
            return render(request, 'inventory/signin_page.html', {
                'not_authenticated': True
            })
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'inventory/signin_page.html')


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('sign-in'))


def sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        existing_user = False
        invalid_request = False
        new_user = False
        if User.objects.filter(username=username):
            existing_user = True
            return render(request, 'inventory/signup_page.html', {
                'existing_user': existing_user
            })

        elif username == '' or password == '':
            invalid_request = True
            return render(request, 'inventory/signup_page.html', {
                'invalid_request': invalid_request
            })

        else:
            new_user = True
            User.objects.create_user(
                username=username,
                password=password
            )
            return render(request, 'inventory/signup_page.html', {
                'new_user': new_user
            })
    else:
        return render(request, 'inventory/signup_page.html')


@login_required
def index(request):
    model = InventoryModel.objects.all()
    low_stock_items = InventoryModel.objects.filter(available_quantity__lt = 3)
    if low_stock_items.exists():
        messages.warning(request,"some item have a quantity less than 3 ")
    return render(request, 'inventory/index.html', {
        'model': model
    })


@login_required
def add_stock(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            product_name= form.cleaned_data['product_name']
            product_description = form.cleaned_data['product_description']
            available_quantity = form.cleaned_data['available_quantity']
            if InventoryModel.objects.filter(product_name=product_name):
                return render(request, 'inventory/add_stock.html', {
                    'form': InventoryForm,
                    'sku_present': True
                })
            else:
                model = InventoryModel(product_name=product_name,product_description = product_description ,available_quantity=available_quantity)
                model.save()
                return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'inventory/add_stock.html', {
            'form': InventoryForm
        })


@login_required
def edit_stock(request, sku):
    model = InventoryModel.objects.get(product_name=sku)
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            model.product_name = form.cleaned_data['product_name']
            model.product_description = form.cleaned_data['product_description']
            model.available_quantity = form.cleaned_data['available_quantity']
            model.save(update_fields=['product_name','product_description','available_quantity'])
            return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)
            return HttpResponseRedirect(reverse('index'))
    else:
        initial = {
            'sku': model.product_name,
            'product_description': model.product_description,
            'available_quantity': model.available_quantity,
        }
        form = InventoryForm(initial=initial)
        return render(request, 'supplier/add_supplier.html', {
            'form': form,
            'sku': sku
        })

@login_required
def delete_stock(request,sku):
    model = InventoryModel.objects.get(product_name=sku)
    model.delete()
    return HttpResponseRedirect(reverse('index'))



def searchproduct(request):
    query = request.GET.get('q')
    if query:
        results = InventoryModel.objects.filter(product_name__icontains=query)
        return render(request, 'inventory/index.html', {
            'model': results
            })
    else:
        return render(request, 'inventory/index.html', {
            'model': []
            })
