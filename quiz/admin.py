from django.contrib import admin
from .models import Quiz, Question, Option, UserAttempt, UserAnswer, Result

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # Show 4 empty option fields by default

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Show 1 empty question field by default

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('question_text', 'quiz', 'question_type')
    list_filter = ('quiz', 'question_type')

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'description', 'duration', 'created_at')

class UserAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'started_at', 'completed_at')

class ResultAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'score')

# Registering all models
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAttempt, UserAttemptAdmin)
admin.site.register(UserAnswer)
admin.site.register(Result, ResultAdmin)
