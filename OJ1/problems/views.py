from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Problem, TestCase
from django.forms.models import inlineformset_factory
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
from .forms import ProblemForm, TestCaseFormSet
from django.forms import modelformset_factory

from .forms import ProblemForm, TestCaseFormSet
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# @login_required
# def add_problem(request):
#     if request.method == 'POST':
#         form = ProblemForm(request.POST)
#         formset = TestCaseFormSet(request.POST, queryset=TestCase.objects.none())

#         if form.is_valid() and formset.is_valid():
#             problem = form.save(commit=False)
#             problem.created_by = request.user
#             problem.save()
#             form.save_m2m()

#             for testcase_form in formset:
#                 if testcase_form.cleaned_data and not testcase_form.cleaned_data.get('DELETE'):
#                     testcase = testcase_form.save(commit=False)
#                     testcase.problem = problem
#                     testcase.save()

#             return redirect('problem-detail', pk=problem.pk)
#     else:
#         form = ProblemForm()
#         formset = TestCaseFormSet(queryset=TestCase.objects.none())

#     return render(request, 'problems/add_problem.html', {'form': form, 'formset': formset})

# from .forms import ProblemForm, TestCaseFormSet

# views.py (in problems app)
# views.py

@login_required
def add_problem(request):
    if request.method == "POST":
        form = ProblemForm(request.POST)
        formset = TestCaseFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            problem = form.save(commit=False)
            problem.created_by = request.user
            problem.save()
            formset.instance = problem
            formset.save()
            return redirect('problem-list')
    else:
        form = ProblemForm()
        formset = TestCaseFormSet()
    return render(request, 'problems/add_problem.html', {'form': form, 'formset': formset, 'heading': 'Add Problem'})

@login_required
def edit_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    form = ProblemForm(request.POST or None, instance=problem)
    formset = TestCaseFormSet(request.POST or None, instance=problem)
    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('problem-list')
    return render(request, 'problems/edit_problem.html', {'form': form, 'formset': formset, 'heading': 'Edit Problem'})
#from django.shortcuts import render, redirect, get_object_or_404
# from .models import Problem
# from .forms import ProblemForm, TestCaseFormSet
# @login_required
# def add_problem(request):
#     if request.method == "POST":
#         form = ProblemForm(request.POST)
#         formset = TestCaseFormSet(request.POST)
#         if form.is_valid() and formset.is_valid():
#             problem = form.save(commit=False)
#             problem.created_by = request.user
#             problem.save()
#             formset.instance = problem
#             formset.save()
#             return redirect('problem-list')
#     else:
#         form = ProblemForm()
#         formset = TestCaseFormSet()
#     return render(request, 'problems/add_problem.html', {'form': form, 'formset': formset})

# @login_required
# def edit_problem(request, pk):
#     problem = get_object_or_404(Problem, pk=pk)
#     form = ProblemForm(request.POST or None, instance=problem)
#     formset = TestCaseFormSet(request.POST or None, instance=problem)
#     if request.method == "POST":
#         if form.is_valid() and formset.is_valid():
#             form.save()
#             formset.save()
#             return redirect('problem-list')
#     return render(request, 'problems/edit_problem.html', {'form': form, 'formset': formset})
# @login_required
# def add_problem(request):
#     if request.method == 'POST':
#         form = ProblemForm(request.POST)
#         formset = TestCaseFormSet(request.POST)
#         if form.is_valid() and formset.is_valid():
#             problem = form.save(commit=False)
#             problem.created_by = request.user
#             problem.save()
#             form.save_m2m()
#             formset.instance = problem
#             formset.save()
#             return redirect('problem-detail', pk=problem.pk)
#     else:
#         form = ProblemForm()
#         formset = TestCaseFormSet()
#     return render(request, 'problems/add_problem.html', {
#         'form': form,
#         'formset': formset,
#         'heading': 'Add Problem'
#     })
# @login_required
# def edit_problem(request, pk):
#     problem = get_object_or_404(Problem, pk=pk, created_by=request.user)
#     if request.method == 'POST':
#         form = ProblemForm(request.POST, instance=problem)
#         formset = TestCaseFormSet(request.POST, instance=problem)
#         if form.is_valid() and formset.is_valid():
#             problem = form.save()
#             instances = formset.save(commit=False)
#             for instance in instances:
#                 instance.problem = problem
#                 instance.save()
#             # Delete any marked test cases
#             for obj in formset.deleted_objects:
#                 obj.delete()
#             return redirect('problem-detail', pk=problem.pk)
#     else:
#         form = ProblemForm(instance=problem)
#         formset = TestCaseFormSet(instance=problem)

#     return render(request, 'problems/edit_problem.html', {
#         'form': form,
#         'formset': formset,
#         'problem': problem,
#         'heading': f'Edit Problem: {problem.title}'
#     })
# def edit_problem(request, pk):
#     problem = get_object_or_404(Problem, pk=pk, created_by=request.user)
#     if request.method == 'POST':
#         form = ProblemForm(request.POST, instance=problem)
#         formset = TestCaseFormSet(request.POST, instance=problem)
#         if form.is_valid() and formset.is_valid():
#             print("Cleaned formset data:")
#             for f in formset:
#                 print(f.cleaned_data)
#             problem = form.save()
#             formset.instance = problem  # ✅ Required to bind new test cases
#             formset.save()
#             return redirect('problem-detail', pk=problem.pk)
#     else:
#         form = ProblemForm(instance=problem)
#         formset = TestCaseFormSet(instance=problem)

#     return render(request, 'problems/edit_problem.html', {
#         'form': form,
#         'formset': formset,
#         'problem': problem,
#         'heading': f'Edit Problem: {problem.title}'
#     })


# @login_required
# def add_problem(request):
#     if request.method == 'POST':
#         form = ProblemForm(request.POST)
#         formset = TestCaseFormSet(request.POST)
#         if form.is_valid() and formset.is_valid():
#             problem = form.save(commit=False)
#             problem.created_by = request.user
#             problem.save()
#             formset.instance = problem
#             formset.save()
#             return redirect('problem-detail', pk=problem.pk)
#     else:
#         form = ProblemForm()
#         formset = TestCaseFormSet()
#     return render(request, 'problems/add_problem.html', {'form': form, 'formset': formset, 'heading': f"Add Problem: {problem.title}",})

# @login_required
# def edit_problem(request, pk):
#     problem = get_object_or_404(Problem, pk=pk, created_by=request.user)
#     if request.method == 'POST':
#         form = ProblemForm(request.POST, instance=problem)
#         formset = TestCaseFormSet(request.POST, instance=problem)
#         if form.is_valid() and formset.is_valid():
#             form.save()
#             formset.save()
#             return redirect('problem-detail', pk=problem.pk)
#     else:
#         form = ProblemForm(instance=problem)
#         formset = TestCaseFormSet(instance=problem)
#     return render(request, 'problems/edit_problem.html', {'form': form, 'formset': formset, 'problem': problem, 'heading': f"Edit Problem: {problem.title}",})
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Problem, TestCase
# from .forms import ProblemForm
# from .forms import TestCaseFormSet
# from django.contrib.auth.decorators import login_required

# @login_required
# def add_problem(request):
#     if request.method == "POST":
#         form = ProblemForm(request.POST, request.FILES)
#         formset = TestCaseFormSet(request.POST)
#         if form.is_valid() and formset.is_valid():
#             problem = form.save(commit=False)
#             problem.created_by = request.user
#             problem.save()
#             formset.instance = problem
#             formset.save()
#             return redirect("problem-detail", pk=problem.pk)
#     else:
#         form = ProblemForm()
#         formset = TestCaseFormSet()

#     return render(request, "problems/add_problem.html", {"form": form, "formset": formset})


# @login_required
# def edit_problem(request, pk):
#     problem = get_object_or_404(Problem, pk=pk, created_by=request.user)
#     if request.method == "POST":
#         form = ProblemForm(request.POST, request.FILES, instance=problem)
#         formset = TestCaseFormSet(request.POST, instance=problem)
#         if form.is_valid() and formset.is_valid():
#             form.save()
#             formset.save()
#             return redirect("problem-detail", pk=problem.pk)
#     else:
#         form = ProblemForm(instance=problem)
#         formset = TestCaseFormSet(instance=problem)

#     return render(request, "problems/edit_problem.html", {"form": form, "formset": formset, "problem": problem})

# @login_required
# def edit_problem(request, pk):
#     problem = get_object_or_404(Problem, pk=pk, created_by=request.user)

#     if request.method == 'POST':
#         form = ProblemForm(request.POST, instance=problem)
#         formset = TestCaseFormSet(request.POST, instance=problem)
#         if form.is_valid() and formset.is_valid():
#             form.save()
#             formset.save()
#             return redirect('problem-detail', pk=pk)
#     else:
#         form = ProblemForm(instance=problem)
#         formset = TestCaseFormSet(instance=problem)

#     return render(request, 'problems/edit_problem.html', {'form': form, 'formset': formset, 'problem': problem})

# @login_required
# def add_problem(request):
#     if request.method == 'POST':
#         form = ProblemForm(request.POST)
#         if form.is_valid():
#             problem = form.save(commit=False)
#             problem.created_by = request.user
#             problem.save()

#             formset = TestCaseFormSet(request.POST, instance=problem)
#             if formset.is_valid():
#                 formset.save()
#                 return redirect('problem-detail', pk=problem.pk)
#     else:
#         form = ProblemForm()
#         formset = TestCaseFormSet()

#     return render(request, 'problems/add_problem.html', {'form': form, 'formset': formset, 'problem': problem})

# @login_required
# def edit_problem(request, pk):
#     problem = get_object_or_404(Problem, pk=pk, created_by=request.user)

#     if request.method == 'POST':
#         form = ProblemForm(request.POST, instance=problem)
#         formset = TestCaseFormSet(request.POST, queryset=TestCase.objects.filter(problem=problem))

#         if form.is_valid() and formset.is_valid():
#             form.save()

#             for testcase_form in formset:
#                 if testcase_form.cleaned_data:
#                     if testcase_form.cleaned_data.get('DELETE'):
#                         if testcase_form.instance.pk:
#                             testcase_form.instance.delete()
#                     else:
#                         testcase = testcase_form.save(commit=False)
#                         testcase.problem = problem
#                         testcase.save()

#             return redirect('problem-detail', pk=problem.pk)
#     else:
#         form = ProblemForm(instance=problem)
#         formset = TestCaseFormSet(queryset=TestCase.objects.filter(problem=problem))

#     return render(request, 'problems/edit_problem.html', {'form': form, 'formset': formset,'problem': problem})

# # @login_required
# def add_problem(request):
#     if not request.user.is_staff and not request.user.userprofile.is_problem_setter:
#         return redirect('problem-list') 

#     if request.method == 'POST':
#         form = ProblemForm(request.POST)
#         if form.is_valid():
#             problem = form.save(commit=False)
#             problem.created_by = request.user
#             problem.save()
#             return redirect('problem-detail', pk=problem.pk)
#     else:
#         form = ProblemForm()
#     return render(request, 'problems/add_problem.html', {'form': form})

# @login_required
# def edit_problem(request, pk):
#     problem = get_object_or_404(Problem, pk=pk)

#     if request.user != problem.created_by and not request.user.is_staff:
#         return redirect('problem-detail', pk=problem.pk)  # or raise PermissionDenied

#     if request.method == 'POST':
#         form = ProblemForm(request.POST, instance=problem)
#         if form.is_valid():
#             form.save()
#             return redirect('problem-detail', pk=problem.pk)
#     else:
#         form = ProblemForm(instance=problem)

#     return render(request, 'problems/edit_problem.html', {'form': form, 'problem': problem})



