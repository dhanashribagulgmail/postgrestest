from django.shortcuts import render
from django.http import HttpResponse
from DonarDetails.models import *
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


def home(request):
     return render(request ,"donar/index.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request ,'Invalid User')
            return redirect('/login/')
        
        user=authenticate(username=username ,password=password) 

        if user is None:
            messages.error(request ,'Invalid Password')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/donar_data/')

    return render(request, "donar/login.html")   


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=User.objects.filter(username=username)

        if user.exists():
            messages.info(request,'Username already exist')
            return redirect('/register/') 

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )

        user.set_password(password)
        user.save()

        messages.info(request,'User Account Created Successfully ')

        return redirect('/register/')

    return render(request, "donar/register.html")


def logout_page(request):
    logout(request)
    return render(request ,"donar/login.html")


@login_required 
def donar_data(request):
    data=request.POST
    if request.method=="POST":
        donar_photo=request.FILES.get('donar_photo')
        print(data)
        name=data.get('name')
        age=data.get('age')
        address=data.get('address')
        email=data.get('email')
        print(name)
        print(email)
        print(donar_photo)


        donar_details.objects.create(
            name=name,
            age=age,
            email=email,
            address=address,
            donar_photo=donar_photo
        )
        
     
        return redirect('/donar_data/')
    
    
    donars = donar_details.objects.all()


    if request.GET.get('search'):
        print(request.GET.get('search'))

        donars= donars.filter(name__icontains = request.GET.get('search'))



    return render(request, "donar/donarDetails.html", {'donar': donars})   

@login_required 
def delete_function(request,id):
    print(id)
    deletedonar=donar_details.objects.get(id=id)
    deletedonar.delete()
    return redirect('/donar_data/')


    
@login_required 
def update_donar_data(request,id):
    print(id)
    queryset=donar_details.objects.get(id=id)   

    context={'donar':queryset}

    if request.method=="POST":
        data=request.POST
        donar_photo=request.FILES.get('donar_photo')
        print(data)
        queryset.name=data.get('name')
        queryset.age=data.get('age')
        queryset.address=data.get('address')
        queryset.email=data.get('email')
        if donar_photo:
            queryset.donar_photo=donar_photo       
       

        queryset.save();
        return redirect('/donar_data/')
    return render(request, "donar/update_donar.html",context )   

