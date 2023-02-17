"""siteweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings  
from django.conf.urls.static import static  
from django.urls import path, include 
from rendez_vous.views import create_appointment, accueil, user_login,register, user_logout


app_name = "siteweb"  
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",accueil,name="accueil"),    
    path("login", user_login, name="login"),
    path("logout", user_logout, name="logout"),      
    path('create-appointment/', create_appointment, name='create-appointment'), 
    # path("dashboard",dashboard, name="dashboard"),   
    # path("today-appointment", today_appointment, name="today-appointment"),  
    # path("all-appointment", all_appointment, name="all-appointment"),  
    path("register/", register, name="register"),
    
]
