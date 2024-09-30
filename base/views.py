from django.shortcuts import render, redirect
from .models import User, Event, Submission
from .forms import SubmissionForm, RegisterCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse



def home(request):
    users = User.objects.filter(hackathon_participant=True)
    events = Event.objects.all()
    
    context = {'users' : users, 'events' : events}
    return render(request, 'home.html', context)



# @login_required(login_url='login_page')
def event(request, id):
    event = Event.objects.get(id=id)
    
    registered = False
    submission = False
    if request.user.is_authenticated:
        registered = request.user.events.filter(id=event.id).exists()
        submission = Submission.objects.filter(participant=request.user, event=event).exists()
    # print('submission:',submission)
    context = {'event' : event, 'registered' : registered, 'submission': submission}
    return render(request, 'event.html', context)

@login_required(login_url='login_page')
def event_confirmation(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        event.participants.add(request.user)
        return redirect('event', id=event.id)
    context = {'event': event}
    return render(request, 'event_confirmation.html', context)

def profile(request, id):
    user = User.objects.get(id=id)
    context = {'user' : user}
    return render(request, 'profile.html', context)


@login_required(login_url='login_page')
def account(request):
    
    user = request.user
    context = {'user': user}
    
    return render(request, 'account.html', context)

@login_required(login_url='login_page')
def submit_form(request, id):
    event = Event.objects.get(id=id)
    form = SubmissionForm()
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.event = event
            submission.participant = request.user
            submission.save()
            return redirect('account')
            
    
    context = {'event' : event, 'form': form}
    return render(request, 'submit_form.html', context)


@login_required(login_url='login_pag')
def update_form(request, id):
    submission = Submission.objects.get(id=id)
    
    if request.user != submission.participant:
        return HttpResponse('You Cant be Here!!!!!')
    
    event = submission.event
    form = SubmissionForm(instance=submission)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')
    
    context  = {'form' : form, 'event' : event}
    return render(request, 'submit_form.html', context)


def login_page(request):
    page = 'login'
    
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.ERROR(request, 'username or password is incorrect')
        
        
    context  = {'page': page}
    return render(request, 'login_page.html', context)


def logout_page(request):
    logout(request)
    return redirect('login_page')
    

def register_page(request):
    page = 'register'
    
    form = RegisterCreationForm()
    if request.method == 'POST':
        form = RegisterCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    
    context  = {'page': page, 'form' : form}
    return render(request, 'login_page.html', context)



# Create your views here.
