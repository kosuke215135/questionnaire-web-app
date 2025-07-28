from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

# 回答タイプ（単一選択・複数選択・記述式など）
class AnswerType(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 例: 'single_choice', 'multiple_choice', 'text'

    def __str__(self):
        return self.name

class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField('公開日')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作成者', null=True, blank=True)

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

class UserProfile(models.Model):
    """ユーザーの詳細情報を管理するモデル"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name='自己紹介')
    birth_date = models.DateField(null=True, blank=True, verbose_name='生年月日')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')

    class Meta:
        verbose_name = 'ユーザープロフィール'
        verbose_name_plural = 'ユーザープロフィール'

    def __str__(self):
        return f"{self.user.username}のプロフィール"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ユーザー作成時にプロフィールを自動作成"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """ユーザー更新時にプロフィールも更新"""
    instance.profile.save()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.CASCADE)  # 選択式用
    text = models.TextField(blank=True)  # 記述式用
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question} by {self.user}"
