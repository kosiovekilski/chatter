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
    user = request.user
    html = "<a href=\"login\"> LOG IN </a> <a href=\"logout\"> LOG OUT </a> you are %s </body></html>" % (request.user)
    return HttpResponse(html)

def logout_view(request):
    logout(request)
    return redirect('../..')

def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render_to_response('index.html', username)
    return redirect('../..')

def send(request):
    if request.method == 'POST':
        message = Message()
        message.from_user = request.user
        message.to_user = get_random_user(request.user)
        message.message = request.POST[u'message_to_random_user']
        message.date = datetime.now()
        message.save()
    return render(request, 'send.html', {'rand_user': get_random_user(request.user)})

def show_my_messages(request):
    messages = Message.objects.all().filter(Q(from_user=request.user) | Q(to_user=request.user)).order_by('-date').distinct()
    users = []
    for o in messages:
        if request.user:
            if not o.get_to_user in users:
                users.append(o.get_to_user)
    r = lambda: random.randint(0,255)
    rand_color = '#%02X%02X%02X' % (r(),r(),r())
    return render(request, 'show.html', {'r': rand_color, 'u': users})

def show_messages_user(request):
    messages = Message.objects.all().get(Q(from_user=request.user, to_user=user) | Q(to_user=request.user, from_user=user)).order_by('-date')
    return render(request, 'all.html', {'u': users})
