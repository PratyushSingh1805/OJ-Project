# from django.contrib import admin

# # Register your models here.
# from .models import Problem, TestCase, Tag

# class TestCaseInline(admin.TabularInline):
#     model = TestCase
#     extra = 1

# #admin.site.register(Problem)
# @admin.register(Problem)
# @admin.register(Tag)
# class ProblemAdmin(admin.ModelAdmin):
#     list_display = ('title', 'difficulty',)
#     search_fields = ('title',)
#     list_filter = ('difficulty','tags')
#     filter_horizontal = ('tags',)
#     inlines = [TestCaseInline]

from django.contrib import admin
from .models import Problem, TestCase, Tag

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'display_tags')
    search_fields = ('title',)
    list_filter = ('difficulty', 'tags')
    filter_horizontal = ('tags',)
    inlines = [TestCaseInline]

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    display_tags.short_description = 'Tags'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
