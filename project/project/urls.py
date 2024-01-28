"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from main.views import *
from authentification.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    
    #PAge d'accueil
    path("home/", accueil,name="accueil"),


    #Connexion
    path("login/", login,name="login"),


    #Inscription
    path("signup/",signup,name='signup'),

    #projects
    path("projects/",projects),

    #How it works
    path("howitworks/",utilisateur,name='utilisateur'),
#pour le formulaire js
    #Recuperer les types d'evenements sous format JSON pour les afficher avec du JS
    path("typeevent-json/",get_type_event,name='typeeventjson'),
    #Recuperer les dates non disponibles de l'equipe passee en parametres sous format JSON
    path("howitworks/team-json/<str:typeEvent>/",get_json_team),
    #recuperer les heures dispo d'une date
    path("howitworks/hour-json/<str:typeEvent>/<str:appDate>/",get_available_hours_for_date),
    


#employe profil
    path("myaccount/<str:email>/",profil,name="myaccount"),

#DASHBORAD
    path("dashboard/",admiin),
    path("dashboard/events/",events),
    path("dashboard/members/",members),
    path('',email),


    path("dashboard/appointments/",appointments),


   # path('get_graph_data/', get_graph_data, name='get_graph_data'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Servir les fichiers média à partir de settings.MEDIA_ROOT 





