from django.shortcuts import render, get_object_or_404

# Create your views here.
from .forms import CodeSubmissionForm
from .utils import run_code
from .models import Submission
from problems.models import Problem
from django.contrib.auth.decorators import login_required
from django.conf import settings
import subprocess, uuid
from pathlib import Path
from django.template import loader
from django.http import HttpResponse

@login_required
def submit_code(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem = problem
            #submission.input_data = problem.sample_input
            test_cases = problem.test_cases.all()
            verdict, results = run_code(submission.language, submission.code, test_cases)

            # verdict, output = run_code(
            #     submission.language,
            #     submission.code,
            #     submission.input_data,
            #     problem.sample_output
            # )
            #submission.output_data = output
            submission.verdict = verdict
            submission.output_data = "\n".join([f"{i+1}) {v}: {o}" for i, (v, o) in enumerate(results)])
            submission.save() 
            #submission.output_data = run_code(submission.language, submission.code, submission.input_data)
            #submission.save()
            #return render(request, "submit/result.html", {"submission": submission})
            template = loader.get_template('result.html')
            context = {'verdict': verdict, 'results': results, 'problem': problem}
            #context = {'submission': submission}
            return HttpResponse(template.render(context, request))
    else:
        form = CodeSubmissionForm()

    #return render(request, "submit/submit.html", {"form": form, "problem": problem})
    template = loader.get_template('submit.html')
    context = {'form': form, 'problem': problem}
    return HttpResponse(template.render(context, request))

@login_required
def submission_history(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    template = loader.get_template('history.html')
    context = {'submissions': submissions}
    return HttpResponse(template.render(context, request))
    #return render(request, 'submit/history.html', {'submissions': submissions})

from django.db.models import Count

@login_required
def leaderboard(request):
    leaderboard_data = (
        Submission.objects.filter(verdict="Accepted")
        .values('user__username')
        .annotate(score=Count('problem', distinct=True))
        .order_by('-score')
    )
    template = loader.get_template('leaderboard.html')
    context = {'leaderboard': leaderboard_data}
    return HttpResponse(template.render(context, request))
    #return render(request, 'submit/leaderboard.html', {'leaderboard': leaderboard_data})


