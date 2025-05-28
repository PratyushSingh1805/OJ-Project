from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from problems.models import Problem

class Submission(models.Model):
    LANGUAGE_CHOICES = [
        ('cpp', 'C++'),
        ('py', 'Python'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    input_data = models.TextField(blank=True)
    output_data = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verdict = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.verdict}"

