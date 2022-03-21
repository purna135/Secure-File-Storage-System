from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from django.contrib import messages
from os import system
import re
import base64
from .face_rec import *
from django.urls import reverse


def indexview(request):
    return render(request, 'index.html')


def signinview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = myuser.objects.get(pk=username, Password=password)
            request.session['username'] = username
            return render(request, 'take_image.html')
        except myuser.DoesNotExist:
            messages.error(request, 'Username and password did not matched')
    return render(request, 'signin.html')


def signupview(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['username'] = form.cleaned_data['Username']
            system(f"mkdir media\\{request.session['username']}")
            return render(request, 'take_image.html')
    else:
        form = RegForm()
    return render(request, 'signup.html', {'form': form})


def logoutview(request):
    try:
        request.session['username']
    except KeyError:
        return HttpResponseRedirect(reverse('indexview'))

    del request.session['username']
    return HttpResponseRedirect(reverse('indexview'))


def save_image( request ):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('signupview'))

    dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
    image_data = request.POST['imagedata']
    image_data = dataUrlPattern.match(image_data).group(2)
    image_data = image_data.encode()
    image_data = base64.b64decode(image_data)

    if request.resolver_match.url_name == 'signup_save_img':
        user = request.session['username']
        with open(f'images/train/{user}.jpg', 'wb') as f:
            f.write(image_data)
        with open(f'user/static/img/{user}.jpg', 'wb') as f:
            f.write(image_data)   

        if face_validation(f'images/train/{user}.jpg'):
            del user
            return render(request, 'index.html', {'mess': 'success'})
        else:
            system(f'del images\\train\\{user}.jpg')
            messages.error(request, "We cann't not recognise your face")
            messages.error(request, "Please take a another pic having your face only...")
            return render(request, 'take_image.html')

    if request.resolver_match.url_name == 'signin_save_img':
        user = request.session['username']
        with open(f'images/test/{user}.jpg', 'wb') as f:
            f.write(image_data)

        if face_validation(f'images/test/{user}.jpg'):
            known_face = f'images/train/{user}.jpg'
            unknown_face = f'images/test/{user}.jpg'

            if match_face(known_face, unknown_face):
                system(f'del images\\test\\{user}.jpg')
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                system(f'del images\\test\\{user}.jpg')
                messages.error(request, "Face does not match...")
                return render(request, 'take_image.html')
        else:
            system(f'del images\\test\\{user}.jpg')
            messages.error(request, "We cann't not recognise your face")
            messages.error(request, "Please take a another pic having your face only...")
            return render(request, 'take_image.html')

    if request.resolver_match.url_name == 'changepass_save_img':
        user = request.session['username']
        with open(f'images/test/{user}.jpg', 'wb') as f:
            f.write(image_data)

        if face_validation(f'images/test/{user}.jpg'):
            known_face = f'images/train/{user}.jpg'
            unknown_face = f'images/test/{user}.jpg'

            if match_face(known_face, unknown_face):
                system(f'del images\\test\\{user}.jpg')
                return HttpResponseRedirect(reverse('updatepass'))
            else:
                system(f'del images\\test\\{user}.jpg')
                messages.error(request, "Face does not match...")
                return render(request, 'take_image.html')
        else:
            system(f'del images\\test\\{user}.jpg')
            messages.error(request, "We cann't not recognise your face")
            messages.error(request, "Please take a another pic having your face only...")
            return render(request, 'take_image.html')



def changepass(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = myuser.objects.get(pk=username)
            request.session['username'] = username
            return render(request, 'take_image.html')
        except myuser.DoesNotExist:
            messages.error(request, 'Username did not matched')
    return render(request, 'changepass.html')



def updatepass(request):
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 == pass2:
            try:
                rec = myuser.objects.filter(Username=request.session['username'])
                del request.session['username']
                rec.update(Password=pass1)
                messages.success(request, "Password Changed Successfully")
                return HttpResponseRedirect(reverse('signinview'))
            except myuser.DoesNotExist:
                messages.error(request, 'Invalid Password')
        else:
            messages.error(request, 'Password Mismatch')
    return render(request, 'updatepass.html')
