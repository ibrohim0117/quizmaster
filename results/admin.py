from django.contrib import admin

from results.models import Result, Answer


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'ball', 'total_questions', 'test_time']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['result', 'question', 'selected_option']

