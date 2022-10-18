from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Authentications, States
from templates import *
from django.contrib.auth.hashers import make_password, check_password
from django.core import mail
# Create your views here.

def index(request):
    if 'isAdmin' in request.session:
        if request.session['isAdmin']==True:
            return redirect('/admin/wall')
        else:
            return redirect('/user/wall')
    else:
        return redirect('/login')

def register(request):
    state_list = States.objects.values()
    context = {
        'state_list': state_list,
    }
    if request.method == "POST":
        errors = Authentications.objects.register_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.add_message(
                    request, messages.ERROR, value, extra_tags='register')
            return render(request, 'auths/register.html',context)
        else:
            state_id = States.objects.get(state=request.POST['state'])

            hash_pw=make_password(request.POST['password'])
            print(hash_pw)
            auth = Authentications.objects.create(
            name=request.POST['name'], email=request.POST['email'], password=hash_pw, state=state_id)
            errors["email"] = "Account is created"
            for key, value in errors.items():
                messages.add_message(
                    request, messages.ERROR, value, extra_tags='register')
            request.session['user_id'] = auth.id
            #sending mail to admin
            # acc_name = request.POST['name']
            # acc_state = request.POST['state']
            # acc_email = "tarun78ak@gmail.com"
            # try:
            #     print("mail sent")
            
            #     connection = mail.get_connection()
            #     connection.open()

            #     email1 = mail.EmailMessage(
            #     'User Request',
            #     '''Dear Admin 
            #         A new user '{}' has sent request for state the '{}'. Kindly look into it.

            #         Thank you.'''.format(acc_name, acc_state),
            #     'proton01sam@proton.me',
            #     [acc_email],
            #     connection=connection,
            #     )
            #     email1.send() # Send the email

                # return render(request, 'auths/register.html',context)
            # except:
            #     print("connection error")
            #     return render(request, 'auths/register.html',context)
    else:
        return render(request, 'auths/register.html',context)

def login(request):
    if request.method == "POST":
        print(request.POST)
        errors = Authentications.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.add_message(
                    request, messages.ERROR, value, extra_tags='login')
            return redirect('/')
        else:
            auth = Authentications.objects.get(email=request.POST['email'])
            request.session['user_id'] = auth.id
            request.session['isAdmin'] = auth.isAdmin

            if request.session['isAdmin']==True:
                return redirect('/admin/wall')
            else:
                return redirect('/user/wall')
    else:
        return render(request, 'auths/login.html')

def reset(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        request.session.clear()
        print("session has been cleared")
        return redirect("/")