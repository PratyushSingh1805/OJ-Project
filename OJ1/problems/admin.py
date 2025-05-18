from django.contrib import admin

# Register your models here.
from .models import Problem

#admin.site.register(Problem)
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'tags')
    search_fields = ('title', 'tags')
    list_filter = ('difficulty',)
