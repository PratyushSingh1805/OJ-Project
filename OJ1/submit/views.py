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
        #print("POST DATA:", request.POST.dict())
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem = problem
            #submission.input_data = problem.sample_input
            test_cases = problem.test_cases.all()
            # verdict, results = run_code(submission.language, submission.code, test_cases)

            # # verdict, output = run_code(
            # #     submission.language,
            # #     submission.code,
            # #     submission.input_data,
            # #     problem.sample_output
            # # )
            # #submission.output_data = output
            # test_case_results = []
            # for i, test_case in enumerate(test_cases):
            #     verdict_label, user_output = results[i]
            #     test_case_results.append({
            #         'verdict': verdict_label,
            #         'passed': verdict_label == 'Accepted',
            #         'expected_output': test_case.expected_output.strip(),
            #         'user_output': user_output.strip(),
            #         'input_data': test_case.input_data.strip(),
            #         #'time': '—',  # You can add timing later if you measure it
            #     })
            verdict, results = run_code(submission.language, submission.code, test_cases)

            test_case_results = []

            if verdict in ["Compilation Error", "Unsupported Language"]:
                test_case_results.append({
                    'verdict': verdict,
                    'passed': False,
                    'expected_output': "",
                    'user_output': results[0][1] if results else "",
                    'input_data': ""
                })
            else:
                for i, test_case in enumerate(test_cases):
                    verdict_label, user_output = results[i]
                    test_case_results.append({
                        'verdict': verdict_label,
                        'passed': verdict_label == 'Accepted',
                        'expected_output': test_case.expected_output.strip(),
                        'user_output': user_output.strip(),
                        'input_data': test_case.input_data.strip(),
                    })

            submission.verdict = verdict
            submission.output_data = "\n".join([f"{i+1}) {v}: {o}" for i, (v, o) in enumerate(results)])
            submission.save() 
            #submission.output_data = run_code(submission.language, submission.code, submission.input_data)
            #submission.save()
            #return render(request, "submit/result.html", {"submission": submission})
            template = loader.get_template('result.html')
            context = {'verdict': verdict, 'results': results, 'problem': problem, 'test_cases': test_case_results,'submission': submission,}
            #context = {'submission': submission}
            return HttpResponse(template.render(context, request))
        else:
            print("Form errors:", form.errors)  # TEMP: log errors
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


import os
import json
import tempfile
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# @csrf_exempt
# @login_required
# def run_code_ajax(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         code = data.get('code', '')
#         language = data.get('language', 'python')
#         custom_input = data.get('custom_input', '')

#         try:
#             with tempfile.NamedTemporaryFile(delete=False, suffix='.py' if language in ['py','python'] else '.cpp') as temp_code_file:
#                 temp_code_file.write(code.encode())
#                 temp_code_file.flush()
#                 temp_code_path = temp_code_file.name

#             if language in ['py','python']:
#                 result = subprocess.run(
#                     ['python', temp_code_path],
#                     input=custom_input.encode(),
#                     capture_output=True,
#                     timeout=5
#                 )
#             else:  # C++
#                 compiled_path = temp_code_path.replace('.cpp', '')
#                 subprocess.run(['g++', temp_code_path, '-o', compiled_path], check=True)
#                 result = subprocess.run(
#                     [compiled_path],
#                     input=custom_input.encode(),
#                     capture_output=True,
#                     timeout=5
#                 )

#             output = result.stdout.decode() + result.stderr.decode()
#         except Exception as e:
#             output = f"Error: {str(e)}"
#         finally:
#             if os.path.exists(temp_code_path):
#                 os.remove(temp_code_path)
#             if language == 'cpp' and os.path.exists(compiled_path):
#                 os.remove(compiled_path)

#         return JsonResponse({'output': output})
@csrf_exempt
@login_required
def run_code_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code', '')
        language = data.get('language', 'python')
        custom_input = data.get('custom_input', '')

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.py' if language in ['py', 'python'] else '.cpp') as temp_code_file:
                temp_code_file.write(code.encode())
                temp_code_file.flush()
                temp_code_path = temp_code_file.name

            if language in ['py', 'python']:
                result = subprocess.run(
                    ['python', temp_code_path],
                    input=custom_input.encode(),
                    capture_output=True,
                    timeout=5
                )
                output = result.stdout.decode()
                error = result.stderr.decode()

                if result.returncode != 0:
                    verdict = "Runtime Error"
                else:
                    verdict = "Success"

            else:  # C++
                compiled_path = temp_code_path.replace('.cpp', '')
                compile = subprocess.run(
                    ['g++', temp_code_path, '-o', compiled_path],
                    capture_output=True
                )
                if compile.returncode != 0:
                    return JsonResponse({
                        'verdict': 'Compilation Error',
                        'output': compile.stderr.decode()
                    })

                result = subprocess.run(
                    [compiled_path],
                    input=custom_input.encode(),
                    capture_output=True,
                    timeout=5
                )
                output = result.stdout.decode()
                error = result.stderr.decode()

                if result.returncode != 0:
                    verdict = "Runtime Error"
                else:
                    verdict = "Success"

        except subprocess.TimeoutExpired:
            verdict = "Time Limit Exceeded"
            output = ""
            error = ""
        except Exception as e:
            verdict = "Error"
            output = str(e)
            error = ""

        finally:
            if os.path.exists(temp_code_path):
                os.remove(temp_code_path)
            if language == 'cpp':
                if os.path.exists(compiled_path):
                    os.remove(compiled_path)

        full_output = output + ("\n" + error if error else "")
        return JsonResponse({
            'verdict': verdict,
            'output': full_output.strip()
        })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json

import google.generativeai as genai

genai.configure(api_key=settings.GEMINI_API_KEY)

@login_required
@csrf_exempt
def ai_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get("code", "")

        prompt = f"Review the following code and provide feedback:\n\n{code}"

        try:
            model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
            response = model.generate_content(prompt)
            review = response.text
        except Exception as e:
            review = f"Error: {str(e)}"

        return JsonResponse({'review': review})

# # views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.conf import settings
# from openai import OpenAI
# import json

# # Create OpenAI client using DeepSeek
# client = OpenAI(
#     api_key=settings.DEEPSEEK_API_KEY,
#     base_url="https://api.deepseek.com/v1"  # DeepSeek uses OpenAI-compatible API
# )

# @csrf_exempt
# @login_required
# def ai_review(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             code = data.get("code", "")
#             prompt = f"Please review the following code and suggest improvements:\n\n{code}"

#             response = client.chat.completions.create(
#                 model="deepseek-chat",  # Or another model like "deepseek-coder"
#                 messages=[
#                     {"role": "system", "content": "You are a helpful code reviewer."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=500,
#                 temperature=0.5,
#             )

#             review = response.choices[0].message.content.strip()
#             return JsonResponse({'review': review})
        
#         except Exception as e:
#             return JsonResponse({'review': f"Error: {str(e)}"})
    
#     return JsonResponse({'review': 'Invalid request method'}, status=400)

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# import openai
# from django.conf import settings

# @login_required
# @csrf_exempt
# def ai_review(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         code = data.get("code", "")

#         prompt = f"Please review the following code and suggest improvements:\n\n{code}"

#         try:
#             openai.api_key = settings.DEEPSEEK_API_KEY
#             openai.api_base = "https://api.deepseek.com"

#             response = openai.ChatCompletion.create(
#                 model="deepseek-chat",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful code reviewer."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=500,
#                 temperature=0.5,
#             )

#             review = response['choices'][0]['message']['content'].strip()
#         except Exception as e:
#             review = f"Error: {str(e)}"

#         return JsonResponse({'review': review})

