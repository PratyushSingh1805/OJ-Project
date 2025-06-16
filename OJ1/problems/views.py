from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Problem

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

from django.shortcuts import render
from .models import Problem, Tag  # Assuming you have a Tag model

def problem_list(request):
    search_query = request.GET.get('q', '')
    difficulty_filter = request.GET.get('difficulty', '')
    tag_filter = request.GET.get('tag', '')

    problems = Problem.objects.all()

    if search_query:
        problems = problems.filter(title__icontains=search_query)

    if difficulty_filter:
        problems = problems.filter(difficulty__iexact=difficulty_filter)

    if tag_filter:
        problems = problems.filter(tags__name__iexact=tag_filter)

    problems = problems.distinct()

    tags = Tag.objects.all()  # For dropdown

    return render(request, 'problem_list.html', {
        'problems': problems.distinct(),
        'search_query': search_query,
        'difficulty_filter': difficulty_filter,
        'tag_filter': tag_filter,
        'tags': tags,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProblemForm
from .models import Problem

@login_required
def add_problem(request):
    if not request.user.is_staff and not request.user.userprofile.is_problem_setter:
        return redirect('problem-list')  # or raise PermissionDenied

    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.created_by = request.user
            problem.save()
            return redirect('problem-detail', pk=problem.pk)
    else:
        form = ProblemForm()
    return render(request, 'problems/add_problem.html', {'form': form})

@login_required
def edit_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)

    if request.user != problem.created_by and not request.user.is_staff:
        return redirect('problem-detail', pk=problem.pk)  # or raise PermissionDenied

    if request.method == 'POST':
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            return redirect('problem-detail', pk=problem.pk)
    else:
        form = ProblemForm(instance=problem)

    return render(request, 'problems/edit_problem.html', {'form': form, 'problem': problem})

# @login_required
# def edit_problem(request, pk):
#     problem = get_object_or_404(Problem, pk=pk)

#     if request.user != problem.created_by and not request.user.is_staff:
#         return redirect('problem-list')  # or raise PermissionDenied

#     if request.method == 'POST':
#         form = ProblemForm(request.POST, instance=problem)
#         if form.is_valid():
#             form.save()
#             return redirect('problem-detail', pk=problem.pk)
#     else:
#         form = ProblemForm(instance=problem)

#     return render(request, 'problems/edit_problem.html', {'form': form})

