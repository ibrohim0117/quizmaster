from django.contrib import admin

from results.models import Result, Answer


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'ball', 'get_total_questions', 'get_percentage', 'get_time_spent', 'start_time', 'end_time']
    list_filter = ['quiz', 'start_time', 'end_time']
    search_fields = ['user__email', 'quiz__name']
    readonly_fields = ['start_time', 'end_time', 'get_test_time', 'get_total_questions', 'get_percentage', 'get_time_spent']
    
    def get_total_questions(self, obj):
        return obj.total_questions
    get_total_questions.short_description = "Jami savollar"
    
    def get_percentage(self, obj):
        return f"{obj.percentage}%"
    get_percentage.short_description = "Foiz"
    
    def get_test_time(self, obj):
        return obj.test_time
    get_test_time.short_description = "Test vaqti"
    
    def get_time_spent(self, obj):
        if obj.time_spent_seconds:
            hours = obj.time_spent_seconds // 3600
            minutes = (obj.time_spent_seconds % 3600) // 60
            seconds = obj.time_spent_seconds % 60
            if hours > 0:
                return f"{hours}s {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            return f"{seconds}s"
        return "-"
    get_time_spent.short_description = "Sarflangan vaqt"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['result', 'question', 'selected_option', 'is_correct', 'get_correct_option']
    list_filter = ['is_correct', 'result__quiz']
    search_fields = ['result__user__email', 'question__question']
    
    def get_correct_option(self, obj):
        correct = obj.question.options.filter(is_true=True).first()
        return correct.option if correct else "-"
    get_correct_option.short_description = "To'g'ri javob"

