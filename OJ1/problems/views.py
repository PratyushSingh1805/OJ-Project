from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Problem

@login_required
def problem_list(request):
    problems = Problem.objects.all()
    #return render(request, 'problems/problem_list.html', {'problems': problems})
    template = loader.get_template('problem_list.html')
    context = {'problems': problems}
    return HttpResponse(template.render(context, request))

@login_required
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    #return render(request, 'problems/problem_detail.html', {'problem': problem})
    template = loader.get_template('problem_detail.html')
    context = {'problem': problem}
    return HttpResponse(template.render(context, request))
