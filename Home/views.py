from django.shortcuts import render, redirect
from accounts.models import *
from django.contrib.auth.models import User
from shopSection.models import *
import os

def index(request):
    categories = Category.objects.all()
    category = request.GET.get('category')
    loc = request.GET.get('loc')
    print(category)
    product = Product.objects.all()
    if loc:
        product = Product.objects.filter(location=loc)
    elif category:
        product = Product.objects.filter(category=category)
    elif request.GET:
        search = request.GET.get('search')
        if search:
            product = Product.objects.filter(name__icontains=search)
        else:
            product = Product.objects.all()
    location = Location.objects.all()
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)[:3]
        cart_count = Cart.objects.filter(user=request.user).count()
    return render(request, "index.html", locals())

def profile(request):

    delete_req = request.GET.get('profile')
    if delete_req:
        delete_user = User.objects.get(id=delete_req)
        delete_user.delete()
        return redirect('register')


    user_id = request.GET.get('profile')
    print(user_id)
    a = request.user
    crnt_User = Profile.objects.get(profUser=a)
    if request.POST:
        dob = request.POST.get('dob')
        num = request.POST.get('phn_num')
        address = request.POST.get('address')
        img = request.FILES.get('img')
        if img != None:
            if len(crnt_User.profPic) > 0:
                if crnt_User.profPic != 'default.jpg':
                    os.remove(crnt_User.profPic.path)
            crnt_User.profPic = img
        if dob != None:
            crnt_User.dob = dob
        if num != None:
            crnt_User.number = num
        if address != None:
            crnt_User.address = address
        crnt_User.save()
        return redirect('profile')
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)[:3]
        cart_count = Cart.objects.filter(user=request.user).count()
    return render(request, 'Profile.html', locals())
