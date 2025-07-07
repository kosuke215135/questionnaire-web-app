from django.db import models

# Create your models here.

class Question(models.Model):
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('公開日')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

# Survey（アンケート）モデルを追加
class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField('公開日')

    def __str__(self):
        return self.title
