from django.contrib import admin

from results.models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'ball', 'total_questions']

