# Use official Python image
FROM python:3.10-slim
# Install system dependencies for compiling C++ code
RUN apt-get update && apt-get install -y \
    g++ \
    python3 \
    python3-pip \
    python3-venv \
    coreutils \
    && apt-get clean
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the full project
COPY . /code/

# Expose Django's default port
EXPOSE 8000

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
