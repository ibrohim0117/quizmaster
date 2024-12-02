from django.contrib import admin

from quiz.models import Quiz, Question, Answer, Science

# Register your models here.

# admin.site.register(Quiz)
# admin.site.register(Question)
# admin.site.register(Answer)
# admin.site.register(Science)

class QuestionStackedInline(admin.StackedInline):
    model = Question
    extra = 1

class AnswerStackedInline(admin.StackedInline):
    model = Answer
    extra = 4

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'degree', 'science']
    search_fields = ['degree', 'science__quiz__name']
    inlines = [QuestionStackedInline, ]


@admin.register(Science)
class ScienceAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'quiz']
    search_fields = ['question']
    inlines = [AnswerStackedInline, ]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer', 'question', 'is_true']


