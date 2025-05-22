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
