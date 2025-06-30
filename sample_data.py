import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from polls.models import Question, Choice

# 仮の質問を作成
q = Question.objects.create(
    question_text="好きな飲み物は？",
    pub_date=timezone.now()
)  # type: ignore

# 仮の選択肢を作成
Choice.objects.create(question=q, choice_text="コーヒー", votes=0)  # type: ignore
Choice.objects.create(question=q, choice_text="紅茶", votes=0)    # type: ignore
Choice.objects.create(question=q, choice_text="水", votes=0)      # type: ignore
Choice.objects.create(question=q, choice_text="ジュース", votes=0) # type: ignore

print("サンプルデータ（飲み物アンケート）の投入が完了しました。") 