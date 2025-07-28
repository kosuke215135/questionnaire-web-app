from django.contrib import admin
from .models import Survey, Question, Choice, Answer, AnswerType, UserProfile, GraphType

# Register your models here.

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'pub_date', 'question_count')
    list_filter = ('pub_date', 'created_by')
    search_fields = ('title', 'description')
    date_hierarchy = 'pub_date'

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = '質問数'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'created_at')
    list_filter = ('created_at', 'birth_date')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'survey', 'answer_type', 'is_required', 'pub_date')
    list_filter = ('answer_type', 'is_required', 'pub_date', 'survey')
    search_fields = ('question_text', 'survey__title')

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'votes')
    list_filter = ('question__survey', 'question__answer_type')
    search_fields = ('choice_text', 'question__question_text')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'choice', 'submitted_at')
    list_filter = ('submitted_at', 'question__survey', 'question__answer_type')
    search_fields = ('question__question_text', 'user__username', 'text')

@admin.register(AnswerType)
class AnswerTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(GraphType)
class GraphTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name')
    search_fields = ('name', 'display_name')
