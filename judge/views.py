from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from judge.models import Question, CodeSubmission
from judge.forms import CodeSubmissionForm
from django.conf import settings
from pathlib import Path
import uuid
import subprocess
import os

@login_required
def all_questions(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'all_question.html', context)

@login_required
def question_details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    output = None
    verdict = None

    if request.method == 'POST':
        if 'run' in request.POST:
            form = CodeSubmissionForm(request.POST)
            if form.is_valid():
                language = form.cleaned_data['language']
                code = form.cleaned_data['code']
                input_data = form.cleaned_data['input_data']
                output = run_code(language, code, input_data)
                return JsonResponse({'output': output})

        elif 'submit' in request.POST:
            form = CodeSubmissionForm(request.POST)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.question = question
                submission.user = request.user
                submission.output_data = run_code(submission.language, submission.code, submission.input_data)
                submission.save()
                verdict = check_test_cases(submission)
                submission.verdict = verdict
                submission.save()
                context = {
                    'question': question,
                    'form': form,
                    'output': submission.output_data,
                    'verdict': verdict,
                }
                return render(request, 'question_details.html', context)

    else:
        form = CodeSubmissionForm()

    context = {
        'question': question,
        'form': form,
    }
    return render(request, 'question_details.html', context)

import os
import subprocess
import uuid
from pathlib import Path
from django.conf import settings

def run_code(language, code, input_data, time_limit=3):
    project_path = Path(settings.BASE_DIR)
    directories = ("codes", "inputs", "outputs")

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    # File extensions based on language
    ext_map = {"cpp": "cpp", "py": "py", "c": "c"}
    code_file_name = f"{unique}.{ext_map[language]}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    try:
        if language == "cpp":
            executable_path = codes_dir / unique
            compile_result = subprocess.run(
                ["g++", str(code_file_path), "-o", str(executable_path)],
                capture_output=True,
                text=True,
                timeout=time_limit
            )
            if compile_result.returncode == 0:
                with open(input_file_path, "r") as input_file:
                    with open(output_file_path, "w") as output_file:
                        subprocess.run(
                            [str(executable_path)],
                            stdin=input_file,
                            stdout=output_file,
                            timeout=time_limit
                        )
        elif language == "c":
            executable_path = codes_dir / unique
            compile_result = subprocess.run(
                ["gcc", str(code_file_path), "-o", str(executable_path)],
                capture_output=True,
                text=True,
                timeout=time_limit
            )
            if compile_result.returncode == 0:
                with open(input_file_path, "r") as input_file:
                    with open(output_file_path, "w") as output_file:
                        subprocess.run(
                            [str(executable_path)],
                            stdin=input_file,
                            stdout=output_file,
                            timeout=time_limit
                        )
        elif language == "py":
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    subprocess.run(
                        ["python", str(code_file_path)],
                        stdin=input_file,
                        stdout=output_file,
                        timeout=time_limit
                    )

        with open(output_file_path, "r") as output_file:
            output_data = output_file.read()
    except subprocess.TimeoutExpired:
        output_data = "Time Limit Exceeded"

    # Clean up
    os.remove(code_file_path)
    os.remove(input_file_path)
    os.remove(output_file_path)
    if language in ["cpp", "c"] and os.path.exists(executable_path):
        os.remove(executable_path)

    return output_data


def check_test_cases(code_submission):
    question = code_submission.question
    test_cases = question.testcase_set.all()
    verdict = "Accepted"
    
    for test_case in test_cases:
        input_data = test_case.input
        expected_output = test_case.expected_output
        user_output = run_code(code_submission.language, code_submission.code, input_data)
        
        
        if user_output.strip() != expected_output.strip():
            verdict = "Rejected"
            break
            
    return verdict
