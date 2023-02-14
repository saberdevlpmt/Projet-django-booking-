from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import User, Event
import hashlib



# Create your views here.
 

def login(request):  
 return render(request,"login.html")  

def create_appointment(request):  
 return render(request,"appoint/create-appointment.html")  



def dashboard(request):  
 return render(request,"index.html")  


def today_appointment(request):  
 return render(request,"today-appointment.html")  


def all_appointment(request):   
 return render(request,"all-appointment.html")  

def register(request):  
 return render(request,"register.html")


#Enregistrement
def register(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
            messages.add_message(request, messages.INFO, 'Utilisateur existe déja avec ce nom.')
            return redirect("App:register")
        except User.DoesNotExist:
            user = User.objects.create(username=username, email=email, password=hashlib.sha512(password.encode()).hexdigest(), date=timezone.now())
            messages.add_message(request, messages.INFO, 'Inscription réussie.')
            return redirect("App:login")
    return render(request,"register.html")


#connexion
def login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
            if hashlib.sha512(password.encode()).hexdigest() == user.password:
                request.session["user"] = {
                    "id": user.id,
                    "username": user.username
                }
                return redirect("App:dashboard")
            else:
                raise Exception()
        except User.DoesNotExist:
            messages.add_message(request, messages.INFO,"Vous avez fourni des identifiants de connexion invalides, veuillez réessayer !", "danger")
            return redirect("App:login")
    return render(request,"login.html")


#rendez-vous
def create_appointment(request):
    if "user" in request.session:
        if request.method=="POST":
            name=request.POST.get("name")
            description=request.POST.get("description")
            time=request.POST.get("time")
            date=request.POST.get("date")
            try:
                event = Event.objects.get(date=date, time=time)
                messages.add_message(request, messages.INFO,"Un événement est déjà programmé pour l'heure spécifiée.")
                return redirect("App:create-appointment")
            except Event.DoesNotExist:
                event = Event(name=name, description=description, time=time, date=date, user=request.session["user"]["username"], status='False')
                event.save()
                messages.add_message(request, messages.INFO, 'Rendez-vous planifié avec succès.')
                return redirect("App:create-appointment")
        return render(request,"appoint/create-appointment.html")
    else:
        return HttpResponseNotFound("Page non accessible")
    
# rendez-vous à venir
 
def today_appointment(request):
    if "user" in request.session:
        username = request.session["user"]["username"]
        appointments = Events.objects.filter(user=username, date=datetime.date.today())
        appointments_count = appointments.count()
        page_number = int(request.GET.get('page', 1))
        appointment = appointments[page_number-1]
        context = {"count":appointments_count, "appointment":appointment, "page_num":page_number, "next_page": min(appointments_count, page_number + 1), "prev_page": max(1, page_number - 1)}
        return render(request, "today-appointment.html", context)
    else:
        return HttpResponseNotFound("Page non accessible")  
    
    
#Terminer  des rendez-vous  

def today_appointment(request):    
    if "user" in request.session:
        appointments = Event.objects.filter(user=request.session["user"]["username"], date=datetime.date.today())
        appointments_count = len(appointments)
        page_number = int(request.GET.get('page', 1))
        appointment = appointments[page_number-1]
        if request.GET.get("complete"):
            appointment.status = True
            appointment.save()
            return redirect("App:today-appointment")
        if request.GET.get("delete"):
            appointment.delete()
            return redirect("App:today-appointment")
        context = {"count":appointments_count,"appointment":appointment,"page_num":page_number, "next_page": min(appointments_count, page_number + 1), "prev_page": max(1, page_number - 1)}
        return render(request, "today-appointment.html", context)
    else:
        return HttpResponseNotFound("Page non accessible")
