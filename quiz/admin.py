from django.contrib import admin

from quiz.models import Quiz, Question, Option, Science

# Register your models here.

# admin.site.register(Quiz)
# admin.site.register(Question)
# admin.site.register(Option)
# admin.site.register(Science)

class OptionStackedInline(admin.StackedInline):
    model = Option
    extra = 4


class QuestionStackedInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'degree', 'science', 'count_questions']
    search_fields = ['degree', 'science__quiz__name']
    inlines = [QuestionStackedInline, ]


@admin.register(Science)
class ScienceAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'quiz']
    search_fields = ['question']
    inlines = [OptionStackedInline, ]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['option', 'question', 'is_true']
    search_fields = ['is_true']




