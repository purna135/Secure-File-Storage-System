from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
# from .forms import *
from django.contrib import auth
from django.contrib import messages
from os import system
import re
import base64
import face_recognition
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import encdec
from home.models import myuser
import os
import time
# Create your views here.


def dashboard(request):
    if request.method == 'POST':
        filename = request.POST['filename']
        enckey = request.POST['enckey']
        file_path = 'media\{}\{}'.format(request.session['username'], filename)
        fd = open(file_path, 'rb')
        data = fd.read()
        fd.close()
        data = base64.b64decode(data)
        if chr(data[0]) == chr(int(enckey)):
            os.system('del "{}"'.format(file_path))
            messages.success(request, "File deleted successfully...")
        else:
            messages.error(request, "Enc Key mismatch. Cann't delete file...")
    try:
        user = request.session['username']
    except KeyError:
        return HttpResponseRedirect(reverse('indexview'))
    path = 'media/' + user
    filelist = os.listdir(path)
    filestorage = counter(filelist)
    print(filestorage)
    return render(request, 'dashboard.html', {'list': filelist, 'filestorage':filestorage})


def upload(request):
    if 'username' in request.session and request.method == 'POST':
        user = request.session['username']
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        if os.path.exists('media/{}/{}'.format(user, myfile.name)):
            x = os.getcwd() +'\\media\\{}\\{}'.format(user, myfile.name)
            os.system('del "' + x + '"')
        filename = fs.save("media/{}/{}".format(user, myfile.name), myfile)
        encdec.encryption( filename , request.POST ['enckey'])
        rec = myuser.objects.filter( Username = user)

        if rec[0].history == None or rec[0].history == [['None']]:
            newhistory =  myfile.name +' saved on' + str (time.ctime())
        else:
            newhistory =  myfile.name +' saved on' + str(time.ctime ()) + '\n' + rec[0].history

        myuser.objects.filter( Username = user).update(history = newhistory)
        messages.success(request, "File Uploaded Successfully")
        return HttpResponseRedirect(reverse('upload'))

    elif 'username' in request.session:
        return render(request, 'upload.html')
    else:
        return HttpResponseRedirect(reverse('indexview'))


def download(request):
    if request.method == 'POST':
        filename = request.POST['filename']
        enckey = request.POST['enckey']
        file_path = 'media/{}/{}'.format(request.session['username'], filename)
        if(encdec . decryption ( file_path , enckey )):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        else:
            messages.error(request, 'Invalid encryption key. Please provide a right key...')
            return HttpResponseRedirect(reverse('download'))
    elif 'username' in request . session :
        user = request.session['username']
        path = 'media/' + user
        filelist = os.listdir(path)
        return render (request , 'download.html', {'list' : filelist})
    else:
        return HttpResponseRedirect(reverse('indexview'))



def history(request):
    if 'username' in request.session:
        rec = myuser.objects.filter(Username = request.session['username'])
        history = rec[0].history

        if history != None and history != '':
            history = history.split('\n')
            history = [ x.split ('saved on') for x in history ]

            for x  in history :
                x [ 0 ] = x[ 0 ]. replace ( request.session['username'] +'/', '')

            return render (request , 'history.html', {'history': history})
        else:
            return render ( request, 'history.html')
    else :
        return HttpResponseRedirect(reverse('indexview'))


def clear_history(request):
    rec = myuser.objects.filter(Username=request.session['username'])
    rec.update(history=None)
    return HttpResponseRedirect(reverse('history'))


def chngpass(request):
    if request.method == 'POST':
        password = request.POST['old_pass']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 == pass2:
            try:
                rec = myuser.objects.filter(Username=request.session['username'], Password=password)
                rec.update(Password=pass1)
                messages.success(request, "Password Changed Successfully")
            except myuser.DoesNotExist:
                messages.error(request, 'Invalid Password')
        else:
            messages.error(request, 'Password Mismatch')
    return render(request, 'chngpass.html')


def profile(request):
    
    return render(request, 'profile.html')


def counter(path):
    image = ['.jpg', '.jpeg', '.png','.gif', '.tif', '.tiff', '.bmp', '.ico', '.svg']
    document = ['.doc', '.docx', '.pdf', '.txt', '.wpd', '.wps', '.rtf']
    music = ['.mp3', '.mpa', '.ogg', '.wav', '.wpl']
    video = ['.3g2', '.3gp', '.avi', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.wmv']

    imgCount =  docCount = mCount = vCount = 0

    imgCount = len([file for imgEx in image for file in path if file.lower().endswith(imgEx)])
    docCount = len([file for docEx in document for file in path if file.lower().endswith(docEx)])
    mCount = len([file for mEx in music for file in path if file.lower().endswith(mEx)])
    vCount = len([file for vEx in video for file in path if file.lower().endswith(vEx)])

    list = {'image':imgCount, 'document':docCount, 'video':vCount, 'music':mCount}
    return list
