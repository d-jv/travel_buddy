from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session:
            messages.error(request,'You must be logged in to acces this section')
            return redirect('/home')
        return func(request, *args, **kwargs)
    return wrapper