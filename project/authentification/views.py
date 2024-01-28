from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.hashers import make_password,check_password
#Utile pour les requetes SQL
from django.db import connection
#Pour recuperer sous format JSON
from django.http import JsonResponse

from datetime import datetime
from django.urls import reverse

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(password)
        with connection.cursor() as cursor:
            # Vérifie si l'utilisateur est un administrateur
            cursor.execute("SELECT password_admin FROM admin WHERE email=%s", [email])
            admin_pass_db = cursor.fetchone()
            
            if admin_pass_db and password == admin_pass_db[0]:
                return redirect( '/dashboard/')
            
            else:    
                # Vérifie si l'utilisateur est un employé
                cursor.execute("SELECT password_emp FROM employee WHERE email_emp=%s", [email])
                employee_pass_db = cursor.fetchone()
                
                if employee_pass_db and password == employee_pass_db[0]:
                    return redirect(reverse('myaccount', kwargs={'email': email}))
              
                     

        return render(request, 'login.html', {'erreur': 'Mot de passe incorrect ou utilisateur inexistant'})

    context = {}
    return render(request, 'login.html', context)


#Ajout membre
def signup(request):
   
    if  request.method=='POST' :
           
            name=request.POST['name']
            email=request.POST['email']
            phone=request.POST['phone']
            team=request.POST['team']
            photo=request.POST['photo']
            password=request.POST['pass']
            

            with connection.cursor() as cursor:
                 cursor.execute("Select 1 from employee Where email_emp=%s",[email])
                 emp= cursor.fetchone()
                 if (emp):
                      return render(request,'members.html',{"exist":"This employee is already registered"})
                 


            # if confirm!=password:
            #     context={'mdp': "Les mots de passe ne sont pas similaires"}
            #     return render(request,'signup.html',context)

           
            
                # Creation d'un objet curseur qui me permettra d'executer des requetes SQL
            with connection.cursor() as cursor:
                #Stocker la requete SQL dans une var

                #&S est juste un parametre de substiution
                    sql_query = """
                    INSERT INTO employee (photo, Id_admin, Type_team, Num_tel,Password_emp,Name_emp,Email_emp)
                    VALUES (%s, %s, %s, %s, %s)"""
                    # Executer la requete
                    cursor.execute(sql_query, [photo,1,team,phone,password, name, email])
                    connection.commit()
    #make_password pour stocker le mdp "hache" dans la bdd
                    context={'Created': True}
                    return render (request,'members.html',context)
    
    #Utilisateur vient de naviguer vers signup
    return render(request,'dashboard.html')




 #Recuperer tous les types d'evenements sous format JSON a partir de la BDD de la table Team
def get_type_event(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Team")  
        result = cursor.fetchall()

    # Format the result into a list of dictionaries
    data = [{'type_team': row[0]} for row in result]

    return JsonResponse({'data': data})



def get_json_team(request,*args,**kwargs):
    #Recuperer a partir de l'HTML l'element avec l'ID "typeEvent"
    selected_type= kwargs.get('typeEvent')

    with connection.cursor() as cursor:
        cursor.execute("(SELECT date_event AS date_a FROM Events WHERE type_team = %s GROUP BY date_event) ",[selected_type]) 

       
        result = cursor.fetchall()

    #Creer un dictionnaire des instances de la table Creneau pour pouvoir les manipuler dans le JS
    data = [{'date_a': row[0]} for row in result]

    print(data)
    return JsonResponse({'data':data})



def get_json_hour(request,*args,**kwargs):
    #Recuperer a partir de l'HTML l'element avec l'ID "typeEvent"
    selected_type= kwargs.get('typeEvent')
    selected_date_str= kwargs.get('appDate')
    selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

    print(selected_type)
    print(selected_date)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Creneau  WHERE type_team=%s AND Creneau.date_a=%s ORDER BY Creneau.heure_a",[selected_type,selected_date]) 

        #Recupere toutes les lignes retournees par la requete SQL et les met dans la variable result 
        result = cursor.fetchall()

    #Creer un dictionnaire des instances de la table Creneau pour pouvoir les manipuler dans le JS
    data = [{'id_creneau': row[0], 'date_a': row[1],'heure_a':row[2],'taken':row[3],'type_team':row[4]} for row in result]

    
    return JsonResponse({'data':data})




def get_available_hours_for_date(request, *args, **kwargs):
    try:
        selected_type = kwargs.get('typeEvent')
        selected_date_str = kwargs.get('appDate')
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except Exception as e:
        print(f"Error parsing date: {e}")
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    # Obtenir les heures déjà présentes dans la table Creneau pour la date spécifiée
    with connection.cursor() as cursor:
        cursor.execute("SELECT Creneau.heure_a FROM Creneau WHERE type_team=%s AND Creneau.date_a=%s ORDER BY Creneau.heure_a", [selected_type, selected_date])

        # Recupere toutes les lignes retournees par la requete SQL et les met dans la variable result
        result = cursor.fetchall()

    # Creer un dictionnaire des instances de la table Creneau pour pouvoir les manipuler dans le JS
    dataa = [{'heure_a': row[0].strftime('%H:%M')} for row in result]

    # Obtenez toutes les heures possibles
    all_hours = ["08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00"]

    # Obtenez les heures disponibles (qui ne sont pas déjà réservées)
    available_hours = [hour for hour in all_hours if hour not in [h['heure_a'] for h in dataa]]

    data = [{'value': hour, 'label': hour} for hour in available_hours]

    # Formattez la réponse JSON pour inclure les heures disponibles
   
    return JsonResponse({'data':data})


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def envoyer_email_avec_template(to, subject, template_path, context):
    # Rendre le contenu HTML du template
    html_content = render_to_string(template_path, context)

    # Envoyer l'e-mail
    send_mail(
        subject,
        '',
        settings.EMAIL_HOST_USER,
        to,
        fail_silently=False,
        html_message=html_content,
    )
    return

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@csrf_exempt
def utilisateur(request):
    
    if  request.method=='POST':
            #client
            email= request.POST.get('Email')
            name=request.POST.get('name')
            phone=request.POST.get('phone')
            #evenement
            eventname=request.POST.get('nomevent')
            type=request.POST.get('type')
            sdateevent=request.POST.get('datee')
            # Convertir en objet datetime
            dateevent_obj = datetime.strptime(sdateevent, '%m/%d/%Y')
            # Reformater dans le format 'YYYY-MM-DD'
            dateevent = dateevent_obj.strftime('%Y-%m-%d')
            description=request.POST.get('description')
            #rdv
            srdv=request.POST.get('datea')

            
            # Convertir en objet datetime
            srdv_obj = datetime.strptime(srdv, '%m/%d/%Y')
            
            # Reformater dans le format 'YYYY-MM-DD'
            rdv = srdv_obj.strftime('%Y-%m-%d')

            heure=request.POST.get('heurea')

                 
            # Creation d'un objet curseur qui me permettra d'executer des requetes SQL
            with connection.cursor() as cursor:
                sql_query = """
                INSERT INTO client (N_tel, Email_client, Name_client)
                VALUES (%s, %s, %s)"""
                cursor.execute(sql_query, [phone, email, name])
                connection.commit()

            
            # Creation d'un objet curseur qui me permettra d'executer des requetes SQL
            with connection.cursor() as cursor:
                un=1
                sql_query = """
                INSERT INTO creneau (heure_a, date_a, type_team,taken)
                VALUES (%s, %s, %s,%s)"""
                # Executer la requete
                cursor.execute(sql_query, [heure, rdv, type,un])
                connection.commit()

                context={'Created': True}

            with connection.cursor() as cursor:
                    cursor.execute("Select id_creneau from creneau Where heure_a=%s AND date_a=%s AND type_team=%s",[heure, rdv, type])
                    #recupere le tuple
                    id= cursor.fetchone()
                    idcreneau=id[0]

            with connection.cursor() as cursor:
                    cursor.execute("Select id_client from client Where Email_client=%s",[email])
                    #recupere le tuple
                    idclient_db= cursor.fetchone()
                    idclient=idclient_db[0]
                  
            # Creation d'un objet curseur qui me permettra d'executer des requetes SQL
            with connection.cursor() as cursor:
                heuree="08:00:00"
                sql_query = """
                INSERT INTO events (type_team, id_client, id_creneau,date_event,heure_event,description,name_event)
                VALUES (%s, %s, %s,%s,%s,%s,%s)"""
                # Executer la requete
                cursor.execute(sql_query, [ type, idclient, idcreneau,dateevent,heuree,description,eventname])
                connection.commit()

                context={'Created': True}   
            subject = "Appointment Confirmation"
            html_message = render_to_string('template.html', {'context_variable': 'value'})  
            plain_message = strip_tags(html_message)

            envoyer_email_avec_template([email],"Appointment Confirmation",'template.html',{'':''})
        
            context = {'Created': True}
            return render(request, 'howitworks.html', context)
    return render(request, 'howitworks.html')


#\\\\\\\\\\\\\\\\\\DASHBOARD\\\\\\\\\\\\\\\\



def email(request):
     
     
          return render(request,"template.html",{'':''})

