from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def register_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request,'User with this username already exists')
            return redirect("/auth/register/")
        
        user = User.objects.create_user(username=username)

        user.set_password(password)

        user.save()
        
        messages.info(request,'User created successfully')
        return redirect('/auth/register/')
    
    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context,request))
    
    

def login_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request,'User with this username does not exist')
            return redirect('/auth/login/')
        
        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request,'invalid password')
            return redirect('/auth/login')
        

        login(request,user)
        messages.info(request,'login successful')

        return redirect('/problems/')
        #return redirect('/auth/login')
        #return redirect('/home/polls/')
    
    template = loader.get_template('login.html')
    context ={}
    return HttpResponse(template.render(context,request))

def logout_user(request):
    logout(request)
    messages.info(request,'logout successful')
    return redirect('/auth/login/')

from django.contrib.auth.decorators import login_required
from submit.models import Submission
from django.shortcuts import render

# @login_required
# def profile_view(request):
#     submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
#     total = submissions.count()
#     accepted = submissions.filter(verdict='Accepted').count()

#     template = loader.get_template('profile.html')
#     context ={
#         'user': request.user,
#         'submissions': submissions,
#         'total': total,
#         'accepted': accepted
#         }
#     return HttpResponse(template.render(context,request))

    # return render(request, 'accounts/profile.html', {
    #     'user': request.user,
    #     'submissions': submissions,
    #     'total': total,
    #     'accepted': accepted
    # })
from django.shortcuts import render
from django.utils.timesince import timesince
from problems.models import Problem
from submit.models import Submission
from django.utils.timesince import timesince
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from submit.models import Submission
from problems.models import Problem
from .models import UserProfile

from .forms import ProfilePicForm

@login_required
def profile_view(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # use the correct name of your URL
    else:
        form = ProfilePicForm(instance=profile)

    submissions = Submission.objects.filter(user=user, verdict='Accepted').select_related('problem')
    solved = set(s.problem.id for s in submissions)
    difficulty_count = {'Easy': 0, 'Medium': 0, 'Hard': 0}
    for prob in Problem.objects.filter(id__in=solved):
        difficulty_count[prob.difficulty] += 1

    context = {
        'user': user,
        'profile': profile,
        'form': form,
        'joined_ago': timesince(user.date_joined).split(',')[0],
        'difficulty_data': difficulty_count,
    }
    template = loader.get_template('profile.html')
    return HttpResponse(template.render(context,request))
    #return render(request, 'accounts/profile.html', context)

# @login_required
# def profile_view(request):
#     user = request.user
#     profile, created = UserProfile.objects.get_or_create(user=user)

#     submissions = Submission.objects.filter(user=user, verdict='Accepted').select_related('problem')

#     # Count problems solved by difficulty
#     solved = set(s.problem.id for s in submissions)
#     difficulty_count = {
#         'Easy': 0,
#         'Medium': 0,
#         'Hard': 0,
#     }
#     for prob in Problem.objects.filter(id__in=solved):
#         difficulty_count[prob.difficulty] += 1

#     context = {
#         'user': user,
#         'profile': profile,
#         'joined_ago': timesince(user.date_joined).split(',')[0],
#         'difficulty_data': difficulty_count,
#     }
#     #return render(request, 'accounts/profile.html', context)
#     template = loader.get_template('profile.html')
#     return HttpResponse(template.render(context,request))

