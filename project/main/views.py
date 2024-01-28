from django.shortcuts import render,redirect
from django.http import HttpResponse
#Utile pour les requetes SQL
from django.db import connection
# Create your views here.
from django.utils import timezone
from django.contrib.auth.hashers import make_password,check_password

def home(request):
    context={}
    return render(request,'index.html',context)

def accueil(request):
    context={}
    return render (request,'accueil.html',context)



def employe(request):
    context={}
    
    return render (request,'employe.html',context)



def projects(request):
    context={}
    with connection.cursor() as cursor:
        sql_query = """
            SELECT *, DATEDIFF(Date_event, CURDATE()) AS days_left
            FROM events
            ORDER BY Date_event DESC;
        """
        cursor.execute(sql_query)
        events = cursor.fetchall()

    # Paginer les résultats
    page = request.GET.get('page', 1)
    paginator = Paginator(events, 8)  # Nombre d'éléments par page

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, affichez la première page
        data = paginator.page(1)
    except EmptyPage:
        # Si la page est hors limites (ex: 9999), affichez la dernière page
        data = paginator.page(paginator.num_pages)

    context['data'] = data

    


    return render (request,'projects.html',context)

def profil(request, email):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name_emp, type_team, Num_tel FROM employee WHERE email_emp=%s", [email])
        employee_info = cursor.fetchone()

    name = employee_info[0]
    team = employee_info[1]
    phone = employee_info[2]


    # Initialisation du contexte
    context = {'email': email, 'name': name, 'team': team, 'phone': phone}

    
    with connection.cursor() as cursor:
            sql_query = """
                SELECT *, DATEDIFF(Date_event, CURDATE()) AS days_left
                FROM events
                WHERE finished=%s AND type_team=%s
                ORDER BY Date_event DESC
                LIMIT 1;
            """
            cursor.execute(sql_query, (0, team))
            result = cursor.fetchone()
    context[f'nextevent'] = result

    
    with connection.cursor() as cursor:
            sql_query = """
                SELECT *
                FROM creneau
                WHERE type_team=%s
                ORDER BY Date_a DESC
                LIMIT 1;
            """
            cursor.execute(sql_query, [team])
            result = cursor.fetchone()
    context[f'app'] = result
    
    with connection.cursor() as cursor:
            sql_query = """
                SELECT *
                FROM events
                WHERE finished=%s AND type_team=%s
                ORDER BY Date_event DESC
                Limit 3;
            """
            cursor.execute(sql_query, (1, team))
            result = cursor.fetchall()

    context[f'event'] = result

    if 'changer' in request.POST:
        
        newphone=request.POST['newPhone']

        with connection.cursor() as cursor:
            # Exécutez votre requête SQL pour mettre à jour l'employé
            cursor.execute("""
                UPDATE employee
                SET Num_tel = COALESCE(%s, Num_tel)
                WHERE email_emp = %s
            """, [newphone,  email])
        

    return render(request, 'employe.html', context)


#||||||||||||||||||DASHBOARD||||||||||||||||||||||||||||


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db import connection

def admiin(request):
    with connection.cursor() as cursor:
        un = 1
        sql_query = """
            SELECT COUNT(Id_event)
            FROM events
            WHERE finished=%s;
        """
        cursor.execute(sql_query, [un])
        archivecountevent = cursor.fetchone()[0]

    with connection.cursor() as cursor:
        zero = 0
        sql_query = """
            SELECT COUNT(Id_event)
            FROM events
            WHERE finished=%s;
        """
        cursor.execute(sql_query, [zero])
        currentevents = cursor.fetchone()[0]

    with connection.cursor() as cursor:
        sql_query = """
            SELECT COUNT(Email_emp)
            FROM employee;
        """
        cursor.execute(sql_query)
        nbremployee = cursor.fetchone()[0]

    with connection.cursor() as cursor:
        current_date = timezone.now().date()
        sql_query = """
            SELECT COUNT(Id_creneau)
            FROM Creneau
            WHERE date_a=%s;
        """
        cursor.execute(sql_query, [current_date])
        nbrrdv = cursor.fetchone()[0]

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Employee")  
        result = cursor.fetchall()

    # Paginate the results
    page = request.GET.get('page', 1)
    paginator = Paginator(result, 4)  # Number of items per page

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, display the first page
        data = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), display the last page
        data = paginator.page(paginator.num_pages)

    with connection.cursor() as cursor:
        zero = 0
        un = 1
        sql_query = """
            SELECT *, DATEDIFF(Date_event, CURDATE()) AS days_left
            FROM events
            WHERE finished=%s
            ORDER BY Date_event DESC
            LIMIT %s;
        """
        cursor.execute(sql_query, [zero, un])
        nextevent = cursor.fetchall()

    context = {
        'archivecountevent': archivecountevent,
        'currentevents': currentevents,
        'nbremployee': nbremployee,
        'nbrrdv': nbrrdv,
        'data': data,  
        'nextevent': nextevent,
        
        
    }
    
    return render(request, 'index.html', context)


from django.http import JsonResponse

def members(request):
    if 'supprimer' in request.POST:
        mail_employee = request.POST['email']
    
    # Exécution de la requête SQL brute
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM employee WHERE email_emp = %s", [mail_employee])
        

    if 'addEmployeeBtn' in request.POST:
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            team = request.POST['team']
            
           # photo = request.POST['photo']
            password = request.POST['password']

            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM employee WHERE email_emp=%s", [email])
                emp = cursor.fetchone()
                un=1
                if emp:
                    return render(request, 'members.html', {"exist": "This employee is already registered"})

                sql_query = """
                    INSERT INTO employee ( Id_admin, Type_team, Num_tel, Password_emp, Name_emp, Email_emp)
                    VALUES ( %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(sql_query, [un, team, phone, password, name, email])
                connection.commit()
    
        

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Employee")  
        result = cursor.fetchall()

    page = request.GET.get('page', 1)
    paginator = Paginator(result, 4)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
               

    context = {'data': data}
    return render(request, 'members.html', context)



def events(request):
    
    if 'supprimer' in request.POST:
        id_event = request.POST['id_event']
        with connection.cursor() as cursor:
            sql_query = """
                DELETE FROM events
                WHERE id_event = %s;
            """
            cursor.execute(sql_query, [id_event])
    if 'modif' in request.POST:
        id_event = request.POST['id_event']
        
        date_event = request.POST['modifyDateEvent']
        name = request.POST['modifyEventName']
        
        desc_event = request.POST['modifyDescEvent']
        # Start building the SQL query
        sql_query = "UPDATE events SET"
        query_params = []

        
        if desc_event:
            sql_query += " description = %s,"
            query_params.append(desc_event)
        
        if date_event:
            sql_query += " date_event = %s,"
            query_params.append(date_event)
        if name:
            sql_query += " name_event = %s,"
            query_params.append(name)

        
        sql_query = sql_query.rstrip(',') + " WHERE id_event = %s;"

        
        query_params.append(id_event)

        
        with connection.cursor() as cursor:
            cursor.execute(sql_query, tuple(query_params))

       

    # Liste des types d'événements
    event_types = ['Birthday', 'Graduation', 'Baby Shower', 'Wedding']

    # Initialisation du contexte
    context = {}

    for event_type in event_types:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT *, DATEDIFF(Date_event, CURDATE()) AS days_left
                FROM events
                WHERE finished=%s AND type_team=%s
                ORDER BY Date_event DESC
                LIMIT 1;
            """
            cursor.execute(sql_query, (0, event_type))
            result = cursor.fetchone()
            context[f'nextevent{event_type.lower()}'] = result

    # Récupération de tous les événements
    with connection.cursor() as cursor:
        sql_query = """
            SELECT *, DATEDIFF(Date_event, CURDATE()) AS days_left
            FROM events
            ORDER BY Date_event DESC;
        """
        cursor.execute(sql_query)
        events = cursor.fetchall()

    # Paginer les résultats
    page = request.GET.get('page', 1)
    paginator = Paginator(events, 4)  # Nombre d'éléments par page

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, affichez la première page
        data = paginator.page(1)
    except EmptyPage:
        # Si la page est hors limites (ex: 9999), affichez la dernière page
        data = paginator.page(paginator.num_pages)

    context['data'] = data
    return render(request, 'events.html', context)



def appointments(request):
    event_types = ['Birthday', 'Wedding', 'Baby Shower', 'Graduation']
    context = {}

    for event_type in event_types:
        with connection.cursor() as cursor:
            sql_query = """
                SELECT creneau.Date_a, creneau.Heure_a, client.email_client, creneau.id_creneau
                FROM events
                JOIN client ON events.Id_client = client.Id_client
                JOIN creneau ON events.Id_creneau = creneau.Id_creneau
                WHERE events.type_team = %s;
            """
            cursor.execute(sql_query, [event_type])
            result = cursor.fetchall()
           
            # Paginer les résultats
            paginator = Paginator(result, 4)  # Nombre d'éléments par page

            # Récupérer la page demandée à partir des paramètres de requête
            page = request.GET.get('page', 1)

            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                # Si la page n'est pas un entier, affichez la première page
                data = paginator.page(1)
            except EmptyPage:
                # Si la page est hors limites (ex: 9999), affichez la dernière page
                data = paginator.page(paginator.num_pages)

            context[f'rdv{event_type.lower()}'] = data
    if 'supprimer' in request.POST:
        id_creneau = request.POST['id']
    
    # Exécution de la requête SQL brute
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM creneau WHERE id_creneau = %s", [id_creneau])
        



    return render(request, 'appointments.html', context)


from django.http import JsonResponse
'''
def get_graph_data(request):
    # Statistique 1: Nombre moyen d'événements par client
    with connection.cursor() as cursor:
        sql_query = """
            SELECT AVG(event_count) as avg_events_per_client
            FROM (
                SELECT COUNT(Id_event) as event_count
                FROM events
                WHERE type_team=%s
                GROUP BY Id_client
            ) AS client_event_counts;
        """
        cursor.execute(sql_query, ["Birthday"])
        moyeventbirth = cursor.fetchone()[0]
        

    # Statistique 2: Nombre total de créneaux par équipe
    with connection.cursor() as cursor:
        sql_query = """
            SELECT T.type_team, COUNT(c.Id_creneau) AS total_creneaux
            FROM Team T
            LEFT JOIN creneau c ON T.type_team = c.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Birthday"])
        birthapp = dict(cursor.fetchall())

    # Statistique 3: Nombre total d'événements par équipe
    with connection.cursor() as cursor:
        sql_query = """
            SELECT T.type_team, COUNT(E.Id_event) AS total_events
            FROM Team T
            LEFT JOIN events E ON T.type_team = E.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Birthday"])
        birthevent = dict(cursor.fetchall())

    # Statistique 4: Nombre total de membres par équipe
    with connection.cursor() as cursor:
        sql_query = """
            SELECT T.type_team, COUNT(E.email_emp) AS total_members
            FROM Team T
            LEFT JOIN Employee E ON T.type_team = E.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Birthday"])
        birthemp = dict(cursor.fetchall())

    # Statistique 1 pour Baby Shower
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT AVG(event_count) as avg_events_per_client
            FROM (
                SELECT COUNT(Id_event) as event_count
                FROM events
                WHERE type_team=%s
                GROUP BY Id_client
            ) AS client_event_counts;
        """
        cursor.execute(sql_query, ["Baby Shower"])
        moyeventbaby = cursor.fetchone()[0]

    # Statistique 2 pour Baby Shower
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT T.type_team, COUNT(c.Id_creneau) AS total_creneaux
            FROM Team T
            LEFT JOIN creneau c ON T.type_team = c.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Baby Shower"])
        babyapp = dict(cursor.fetchall())

    # Statistique 3 pour Baby Shower
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT T.type_team, COUNT(E.Id_event) AS total_events
            FROM Team T
            LEFT JOIN events E ON T.type_team = E.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Baby Shower"])
        babyevent = dict(cursor.fetchall())

    # Statistique 4 pour Baby Shower
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT T.type_team, COUNT(E.email_emp) AS total_members
            FROM Team T
            LEFT JOIN Employee E ON T.type_team = E.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Baby Shower"])
        babyemp = dict(cursor.fetchall())

    # Statistique 1 pour Wedding
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT AVG(event_count) as avg_events_per_client
            FROM (
                SELECT COUNT(Id_event) as event_count
                FROM events
                WHERE type_team=%s
                GROUP BY Id_client
            ) AS client_event_counts;
        """
        cursor.execute(sql_query, ["Wedding"])
        moyeventwedding = cursor.fetchone()[0]

    # Statistique 2 pour Wedding
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT T.type_team, COUNT(c.Id_creneau) AS total_creneaux
            FROM Team T
            LEFT JOIN creneau c ON T.type_team = c.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Wedding"])
        weddingapp = dict(cursor.fetchall())

    # Statistique 3 pour Wedding
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT T.type_team, COUNT(E.Id_event) AS total_events
            FROM Team T
            LEFT JOIN events E ON T.type_team = E.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Wedding"])
        weddingevent = dict(cursor.fetchall())

    # Statistique 4 pour Wedding
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT T.type_team, COUNT(E.email_emp) AS total_members
            FROM Team T
            LEFT JOIN Employee E ON T.type_team = E.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Wedding"])
        weddingemp = dict(cursor.fetchall())

    # Statistique 1 pour Graduation
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT AVG(event_count) as avg_events_per_client
            FROM (
                SELECT COUNT(Id_event) as event_count
                FROM events
                WHERE type_team=%s
                GROUP BY Id_client
            ) AS client_event_counts;
        """
        cursor.execute(sql_query, ["Graduation"])
        moyeventgraduation = cursor.fetchone()[0]

    # Statistique 2 pour Graduation
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT T.type_team, COUNT(c.Id_creneau) AS total_creneaux
            FROM Team T
            LEFT JOIN creneau c ON T.type_team = c.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Graduation"])
        graduationapp = dict(cursor.fetchall())

    # Statistique 3 pour Graduation
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT T.type_team, COUNT(E.Id_event) AS total_events
            FROM Team T
            LEFT JOIN events E ON T.type_team = E.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Graduation"])
        graduationevent = dict(cursor.fetchall())

    # Statistique 4 pour Graduation
    with connection.cursor() as cursor:
        sql_query = """
           
            SELECT T.type_team, COUNT(E.email_emp) AS total_members
            FROM Team T
            LEFT JOIN Employee E ON T.type_team = E.type_team
            WHERE T.type_team=%s
            GROUP BY T.type_team;
        """
        cursor.execute(sql_query, ["Graduation"])

        graduationemp = dict(cursor.fetchall())

    chart_data = {
        'Birthday': [birthapp, moyeventbirth, birthevent, birthemp],
        'Baby Shower': [babyapp, moyeventbaby, babyevent, babyemp],
        'Wedding': [weddingapp, moyeventwedding, birthevent, weddingemp],
        'Graduation': [graduationapp, moyeventgraduation, birthevent, graduationemp],
    }

    return JsonResponse(chart_data)
'''