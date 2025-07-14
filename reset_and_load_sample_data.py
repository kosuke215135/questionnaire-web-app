import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from polls.models import Answer, Choice, Question, Survey, AnswerType

# 既存データ削除
Answer.objects.all().delete()
Choice.objects.all().delete()
Question.objects.all().delete()
Survey.objects.all().delete()
AnswerType.objects.all().delete()