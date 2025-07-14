from django.db import models
from django.contrib.auth import get_user_model

# 回答タイプ（単一選択・複数選択・記述式など）
class AnswerType(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 例: 'single_choice', 'multiple_choice', 'text'

    def __str__(self):
        return self.name

class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField('公開日')

    def __str__(self):
        return self.title

class Question(models.Model):
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('公開日')
    answer_type = models.ForeignKey(AnswerType, on_delete=models.PROTECT)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

User = get_user_model()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.CASCADE)  # 選択式用
    text = models.TextField(blank=True)  # 記述式用
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question} by {self.user}"
