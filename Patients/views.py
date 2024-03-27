from django.shortcuts import render
from django.http import HttpResponse
from Patients.models import *
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


def home(request):
     return render(request ,"home/index.html")


@login_required 
def dynamic_data(request):
    people = [
        {'name': 'Dhanashri K', 'age': 27},
        {'name': 'Radha B', 'age': 27},
        {'name': 'Avinash K', 'age': 12},
        {'name': 'Dattatraya K', 'age': 27},
    ]

    return render(request, "home/index.html", context={'peoples': people})

@login_required 
def patient_data(request):
    data=request.POST
    if request.method=="POST":
        patient_photo=request.FILES.get('patient_photo')
        print(data)
        name=data.get('name')
        age=data.get('age')
        address=data.get('address')
        email=data.get('email')
        print(name)
        print(email)
        print(patient_photo)


        Patient.objects.create(
            name=name,
            age=age,
            email=email,
            address=address,
            patient_photo=patient_photo
        )
        
     
        return redirect('/patient_data/')
    
    
    patients = Patient.objects.all()


    if request.GET.get('search'):
        print(request.GET.get('search'))

        patients= patients.filter(name__icontains = request.GET.get('search'))



    return render(request, "home/patient_details.html", {'patients': patients})   

@login_required 
def delete_function(request,id):
    print(id)
    deletepatient=Patient.objects.get(id=id)
    deletepatient.delete()
    return redirect('/patient_data/')


    
@login_required 
def update_patient_data(request,id):
    print(id)
    queryset=Patient.objects.get(id=id)   

    context={'patients':queryset}

    if request.method=="POST":
        data=request.POST
        patient_photo=request.FILES.get('patient_photo')
        print(data)
        queryset.name=data.get('name')
        queryset.age=data.get('age')
        queryset.address=data.get('address')
        queryset.email=data.get('email')
        if patient_photo:
            queryset.patient_photo=patient_photo       
       

        queryset.save();
        return redirect('/patient_data/')
    return render(request, "home/update_patient.html",context )   

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
            return redirect('/patient_data/')


        



    return render(request, "home/login.html")   


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

    return render(request, "home/register.html")


def logout_page(request):
    logout(request)
    return render(request ,"home/login.html")