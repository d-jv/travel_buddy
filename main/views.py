from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, HttpResponse
from .models import *
from django.db.utils import IntegrityError
from django.contrib import messages
import bcrypt
from .decorators import *
from time import gmtime, strftime, localtime




def home(request):
    data = {}
    return render(request, 'home.html', data)

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, 'Wrong user/password')
        return redirect('/home')

        # si llegamos acá, estamos seguros que al  menos el usuario SI existe
    if  not bcrypt.checkpw(password.encode(), user.password.encode()): 
        messages.error(request, "Wrong user/password")
        return redirect('/home')
    
        # si llegamos hasta acá, estamos seguros que es el usuario y la contraseña está correcta
    request.session['user'] = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'avatar': user.avatar
    }
    messages.success(request, f'Hello there, {user.first_name} {user.last_name}!')
    return redirect('/')

def logout(request):
    del request.session['user']
    return redirect('/home')

def create_account(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    else:
        # si llega por un POST, tomar valores del formulario
        # y crear un nuevo usuario
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_check = request.POST['password_check']

        # validar que el formulario esté correcto
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            # en este caso, hay al menos 1 error en el formulario
            # voy a mostrarle los errores al usuario
            for llave, mensaje_de_error in errors.items():
                messages.error(request, mensaje_de_error)
        
            return redirect('/home')
        
        # si llegamos hasta acá, estamos seguros que ambas coinciden
        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            )
            request.session['user'] = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'avatar': user.avatar
            }
            messages.success(request, 'User successfully created')
            messages.success(request, f'Welcome to Travel Buddy, {user.first_name} {user.last_name}.')
            return redirect('/')
        except IntegrityError:
            messages.error(request, 'This email is already in use')
            return redirect(request.META.get('HTTP_REFERER'))

@login_required
def index(request):
    user_session = request.session['user']
    user = User.objects.get(email=user_session['email'])
    all_trips = Travel.objects.all().order_by('-date_from')
    inHere = [travel.id for travel in user.travels.all()]
    notHere = [travel for travel in Travel.objects.all() if travel.id not in inHere]
    data = {
        'trips': user.travels.all(),
        'other_trips': notHere,
    }
    return render(request, 'index.html', data)

@login_required
def add(request):
    data = {
    }
    return render(request, 'add.html', data)

@login_required
def travels(request, trip_id):
    travel = Travel.objects.get(id=int(trip_id))
    data = {
        # "travel" : Travel.objects.get(id=int(trip_id)),
        "travel" : travel,
        "travelers" : travel.travelers.all()
    }
    return render(request, 'travels.html', data)

@login_required
def add_travel(request):
    errors = Travel.objects.basic_validator(request.POST)
    if len(errors) > 0:
        # en este caso, hay al menos 1 error en el formulario
        # voy a mostrarle los errores al usuario
        for llave, mensaje_de_error in errors.items():
            messages.error(request, mensaje_de_error)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        user_session = request.session['user']
        user = User.objects.get(email=user_session['email'])
        destination = request.POST['destination']
        description = request.POST['description']
        date_from = request.POST['date_from']
        date_to = request.POST['date_to']
        new_travel = Travel.objects.create(
            destination = destination,
            description = description,
            date_from = date_from,
            date_to = date_to,
            user = user,
        )
        new_travel.travelers.add(user)
        messages.success(request, 'Travel successfully created')
        return redirect('/')

@login_required
def cancel(request, trip_id):
    user_session = request.session['user']
    user = User.objects.get(email=user_session['email'])
    travel = Travel.objects.get(id=int(trip_id))
    travel.travelers.remove(user)
    messages.warning(request, 'Your participation in this trip has been canceled.')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def join(request, trip_id):
    user_session = request.session['user']
    user = User.objects.get(email=user_session['email'])
    travel = Travel.objects.get(id=int(trip_id))
    travel.travelers.add(user)
    messages.success(request, 'You just joined this trip. Enjoy!')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def delete(request, trip_id):
    travel = Travel.objects.get(id=int(trip_id))
    travel.delete()
    messages.error(request, 'Trip successfully deleted')
    return redirect(request.META.get('HTTP_REFERER'))