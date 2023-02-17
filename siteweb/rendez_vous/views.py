import datetime
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import User, Event
from .forms import RegisterForm, Login, EventForm
import hashlib



# Create your views here.



def accueil(request):
    return render(request,"accueil.html")




 


def today_appointment(request):  
 return render(request,"today-appointment.html")  


def all_appointment(request):   
 return render(request,"all-appointment.html")  


#Enregistrement

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

#connexion

def user_login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            # Extract the cleaned data from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authenticate the user using Django's built-in authentication system
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Log in the user using Django's built-in login system
                login(request, user)
                # Redirect the user to a success page (e.g., home page)
                return redirect('accueil')
            else:
                # Return an error message if the authentication failed
                form.add_error(None, "nom d'utlisation ou mot de passe incorrect")
    else:
        # If the request method is not POST, create a new form instance
        form = Login()
    return render(request, 'login.html', {'form': form})

#déconnexion

def user_logout(request):
   logout(request)
   return redirect("accueil")


#rendez-vous


 
def create_appointment(request):
    if not request.user.is_authenticated:
        return redirect('login') # ou n'importe quelle page de connexion

    form = EventForm(request.POST or None)
    if form.is_valid():
        event = form.save(commit=False)
        event.user = request.user
        event.save()
        return redirect('accueil')

    context = {'form': form}
    return render(request, 'create_appointment.html', context) 
    
# rendez-vous à venir fonctionnalité future
 
def today_appointment(request):
    if "user" in request.session:
        username = request.session["user"]["username"]
        appointments = Event.objects.filter(user=username, date=datetime.date.today())
        appointments_count = appointments.count()
        page_number = int(request.GET.get('page', 1))
        appointment = appointments[page_number-1]
        context = {"count":appointments_count, "appointment":appointment, "page_num":page_number, "next_page": min(appointments_count, page_number + 1), "prev_page": max(1, page_number - 1)}
        return render(request, "today-appointment.html", context)
    else:
        return HttpResponseNotFound("Page non accessible")  
    
    
#Terminer  des rendez-vous  fonctionnalité future

def today_appointment(request):    
    if "user" in request.session:
        appointments = Event.objects.filter(user=request.session["user"]["username"], date=datetime.date.today())
        appointments_count = len(appointments)
        page_number = int(request.GET.get('page', 1))
        appointment = appointments[page_number-1]
        if request.GET.get("complete"):
            appointment.status = True
            appointment.save()
            return redirect("siteweb:today-appointment")
        if request.GET.get("delete"):
            appointment.delete()
            return redirect("siteweb:today-appointment")
        context = {"count":appointments_count,"appointment":appointment,"page_num":page_number, "next_page": min(appointments_count, page_number + 1), "prev_page": max(1, page_number - 1)}
        return render(request, "today-appointment.html", context)
    else:
        return HttpResponseNotFound("Page non accessible")
    
    
#Afficher tous les rendez-vous fonctionnalité future

def all_appointment(request):
    if "user" in request.session:
        appointments = Event.objects.filter(user=request.session["user"]["username"])
        appointments_count = appointments.count()
        page_number = int(request.GET.get('page', 1))
        appointment = appointments[page_number - 1]
        if request.GET.get("delete"):
            appointment.delete()
            return redirect("siteweb:all-appointment")
        context={"count":appointments_count,"appointment":appointment, "next_page": min(appointments_count, page_number + 1), "prev_page": max(1, page_number - 1)}
        return render(request,"all-appointment.html",context)
    else:
        return HttpResponseNotFound("Page non accessible")  
