from django.contrib import admin

# Register your models here.
from .models import Problem, TestCase

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

#admin.site.register(Problem)
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'tags')
    search_fields = ('title', 'tags')
    list_filter = ('difficulty',)
    inlines = [TestCaseInline]
