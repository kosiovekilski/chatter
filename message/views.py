from django.shortcuts import render, render_to_response,redirect
from models import Message
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import send_message
from datetime import *
import random
from django.db.models import Q

def get_random_user(user):
    rand_user = User.objects.all().order_by('?').first()
    while rand_user == user or rand_user == 'admin':
		rand_user = User.objects.all().order_by('?').first()
    return rand_user

def home(request):
    if request.user.is_authenticated():
        return render_to_response('index.html')
    return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('../..')

def login_user(request):
    username_ = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username_, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('../..')
        else:
            return render_to_response('login.html')
    else:
        return render_to_response('login.html')

def send(request):
    if request.method == 'POST':
        if len(request.POST[u'message_to_random_user']):
            message = Message()
            message.from_user = request.user
            message.to_user = get_random_user(request.user)
            message.message = request.POST[u'message_to_random_user']
            message.date = datetime.now()
            message.save()
    return render(request, 'send.html', {'rand_user': get_random_user(request.user)})

def show_my_messages(request):
    messages = Message.objects.filter(from_user=request.user)
    messages = messages.order_by('-date').distinct()
    return render(request, 'show.html', {'m': messages})

def show_messages_user(request):
    messages = Message.objects.all().get(Q(from_user=request.user, to_user=user) | Q(to_user=request.user, from_user=user)).order_by('-date')
    return render(request, 'all.html', {'u': users})

def answer_to(request):
    if request.method == 'POST':
        ans = Answer()
        ans.message = message
        ans.message = request.POST[u'answerto']
        ans.date = datetime.now()
        ans.save()
    return render(request, 'send.html', {'rand_user': get_random_user(request.user)})
