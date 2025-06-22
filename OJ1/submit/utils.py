import subprocess
import uuid
from pathlib import Path
from django.conf import settings
def run_code(language, code, test_cases):
    import subprocess
    import uuid
    from pathlib import Path
    from django.conf import settings

    language = language.lower()
    if language == "py":
        extension = "py"
    elif language == "cpp":
        extension = "cpp"
    else:
        return "Unsupported Language", [("Unsupported Language", "")]

    base_dir = Path(settings.BASE_DIR)
    codes_dir = base_dir / "codes"
    inputs_dir = base_dir / "inputs"
    outputs_dir = base_dir / "outputs"

    for dir_ in [codes_dir, inputs_dir, outputs_dir]:
        dir_.mkdir(exist_ok=True)

    uid = str(uuid.uuid4())
    code_file = codes_dir / f"{uid}.{extension}"
    executable = codes_dir / uid  # for C++

    code_file.write_text(code)

    # Compilation for C++
    if language == "cpp":
        compile = subprocess.run(
            ["g++", str(code_file), "-o", str(executable)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if compile.returncode != 0:
            return "Compilation Error", [("Compilation Error", compile.stderr.decode())]

    results = []

    for i, test_case in enumerate(test_cases):
        input_file = inputs_dir / f"{uid}_{i}.txt"
        output_file = outputs_dir / f"{uid}_{i}.txt"
        input_file.write_text(test_case.input_data)

        try:
            if language == "py":
                with open(input_file, "r") as stdin, open(output_file, "w") as stdout:
                    result = subprocess.run(
                        ["python", str(code_file)],
                        stdin=stdin,
                        stdout=stdout,
                        stderr=subprocess.PIPE,
                        timeout=5
                    )
            else:  # cpp
                with open(input_file, "r") as stdin, open(output_file, "w") as stdout:
                    result = subprocess.run(
                        [str(executable)],
                        stdin=stdin,
                        stdout=stdout,
                        stderr=subprocess.PIPE,
                        timeout=5
                    )

            output_data = output_file.read_text().strip()
            expected_output = test_case.expected_output.strip()

            if result.returncode != 0:
                results.append(("Runtime Error", result.stderr.decode()))
            elif output_data == expected_output:
                results.append(("Accepted", output_data))
            else:
                results.append(("Wrong Answer", output_data))

        except subprocess.TimeoutExpired:
            results.append(("Time Limit Exceeded", ""))

    overall_verdict = "Accepted" if all(r[0] == "Accepted" for r in results) else "Failed"
    return overall_verdict, results

# def run_code(language, code, test_cases):
#     language = language.lower()
#     if language in ["py", "python"]:
#         extension = "py"
#     elif language == "cpp":
#         extension = "cpp"
#     else:
#         return "Unsupported Language", []
#     base_dir = Path(settings.BASE_DIR)
#     codes_dir = base_dir / "codes"
#     inputs_dir = base_dir / "inputs"
#     outputs_dir = base_dir / "outputs"

#     for dir_ in [codes_dir, inputs_dir, outputs_dir]:
#         dir_.mkdir(exist_ok=True)

#     uid = str(uuid.uuid4())
#     code_file = codes_dir / f"{uid}.{extension}"
#     executable = codes_dir / uid  # for C++

#     code_file.write_text(code)

#     if language == "cpp":
#         compile = subprocess.run(
#             ["g++", str(code_file), "-o", str(executable)],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#         )
#         if compile.returncode != 0:
#             return "Compilation Error", [compile.stderr.decode()]

#     results = []

#     for i, test_case in enumerate(test_cases):
#         input_file = inputs_dir / f"{uid}_{i}.txt"
#         output_file = outputs_dir / f"{uid}_{i}.txt"

#         input_file.write_text(test_case.input_data)
#         expected_output = test_case.expected_output.strip()

#         try:
#             if language in ["py", "python"]:
#                 with open(input_file, "r") as stdin, open(output_file, "w") as stdout:
#                     subprocess.run(["python", str(code_file)], stdin=stdin, stdout=stdout, stderr=subprocess.DEVNULL, timeout=5)

#             elif language == "cpp":
#                 with open(input_file, "r") as stdin, open(output_file, "w") as stdout:
#                     subprocess.run([str(executable)], stdin=stdin, stdout=stdout, stderr=subprocess.DEVNULL, timeout=5)

#             output_data = output_file.read_text().strip()

#             if output_data == expected_output:
#                 results.append(("Accepted", output_data))
#             else:
#                 results.append(("Wrong Answer", output_data))

#         except subprocess.TimeoutExpired:
#             results.append(("Time Limit Exceeded", ""))
#         except Exception as e:
#             results.append(("Runtime Error", str(e)))

#     # If all are accepted, return final verdict
#     if all(r[0] == "Accepted" for r in results):
#         return "Accepted", results
#     else:
#         return "Failed", results


# def run_code(language, code, test_cases):
#     base_dir = Path(settings.BASE_DIR)
#     codes_dir = base_dir / "codes"
#     inputs_dir = base_dir / "inputs"
#     outputs_dir = base_dir / "outputs"

#     for dir_ in [codes_dir, inputs_dir, outputs_dir]:
#         dir_.mkdir(exist_ok=True)

#     uid = str(uuid.uuid4())
#     code_file = codes_dir / f"{uid}.{language}"
#     #input_file = inputs_dir / f"{uid}.txt"
#     #output_file = outputs_dir / f"{uid}.txt"
#     executable = codes_dir / uid  # for C++

#     code_file.write_text(code)
#     #input_file.write_text(input_data)

#     try:
#         if language == "py":
#             # Run Python code
#             with open(input_file, "r") as stdin, open(output_file, "w") as stdout:
#                 subprocess.run(
#                     ["python", str(code_file)],
#                     stdin=stdin,
#                     stdout=stdout,
#                     stderr=subprocess.DEVNULL,
#                     timeout=5,
#                 )

#         elif language == "cpp":
#             # Compile C++ code
#             compile = subprocess.run(
#                 ["g++", str(code_file), "-o", str(executable)],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#             )
#             if compile.returncode != 0:
#                 return "Compilation Error", compile.stderr.decode()

#             # Execute C++ binary
#             with open(input_file, "r") as stdin, open(output_file, "w") as stdout:
#                 subprocess.run(
#                     [str(executable)],
#                     stdin=stdin,
#                     stdout=stdout,
#                     stderr=subprocess.DEVNULL,
#                     timeout=5,
#                 )

#         else:
#             return "Error", "Unsupported language"

#         # Compare output
#         output_data = output_file.read_text().strip()
#         sample_output = sample_output.strip()

#         if output_data == sample_output:
#             return "Accepted", output_data
#         else:
#             return "Wrong Answer", output_data

#     except subprocess.TimeoutExpired:
#         return "Time Limit Exceeded", ""
#     except Exception as e:
#         return "Runtime Error", str(e)

'''
from django.conf import settings
import subprocess, uuid
from pathlib import Path

def run_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    for dir in [codes_dir, inputs_dir, outputs_dir]:
        dir.mkdir(parents=True, exist_ok=True)

    unique = str(uuid.uuid4())
    code_file = codes_dir / f"{unique}.{language}"
    input_file = inputs_dir / f"{unique}.txt"
    output_file = outputs_dir / f"{unique}.txt"

    code_file.write_text(code)
    input_file.write_text(input_data)

    if language == "cpp":
        executable = codes_dir / unique
        compile = subprocess.run(["g++", str(code_file), "-o", str(executable)])
        if compile.returncode == 0:
            with open(input_file) as stdin, open(output_file, "w") as stdout:
                subprocess.run([str(executable)], stdin=stdin, stdout=stdout)
    elif language == "py":
        with open(input_file) as stdin, open(output_file, "w") as stdout:
            subprocess.run(["python3", str(code_file)], stdin=stdin, stdout=stdout)

    return output_file.read_text()
'''
