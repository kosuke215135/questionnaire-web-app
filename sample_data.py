import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from polls.models import Survey, Question, Choice

# サーベイ（アンケート）を作成
survey = Survey.objects.create(
    title="好きなものアンケート",
    description="みんなの好みを調査します",
    pub_date=timezone.now()
)  # type: ignore

# 1つ目の質問
q1 = Question.objects.create(
    survey=survey,
    question_text="好きな飲み物は？",
    pub_date=timezone.now()
)  # type: ignore
Choice.objects.create(question=q1, choice_text="コーヒー", votes=0)  # type: ignore
Choice.objects.create(question=q1, choice_text="紅茶", votes=0)    # type: ignore
Choice.objects.create(question=q1, choice_text="水", votes=0)      # type: ignore
Choice.objects.create(question=q1, choice_text="ジュース", votes=0) # type: ignore

# 2つ目の質問
q2 = Question.objects.create(
    survey=survey,
    question_text="好きな季節は？",
    pub_date=timezone.now()
)  # type: ignore
Choice.objects.create(question=q2, choice_text="春", votes=0)  # type: ignore
Choice.objects.create(question=q2, choice_text="夏", votes=0)  # type: ignore
Choice.objects.create(question=q2, choice_text="秋", votes=0)  # type: ignore
Choice.objects.create(question=q2, choice_text="冬", votes=0)  # type: ignore

# 3つ目の質問
q3 = Question.objects.create(
    survey=survey,
    question_text="好きなペットは？",
    pub_date=timezone.now()
)  # type: ignore
Choice.objects.create(question=q3, choice_text="犬", votes=0)  # type: ignore
Choice.objects.create(question=q3, choice_text="猫", votes=0)  # type: ignore
Choice.objects.create(question=q3, choice_text="鳥", votes=0)  # type: ignore
Choice.objects.create(question=q3, choice_text="魚", votes=0)  # type: ignore

print("サンプルデータ（アンケート＋複数質問）の投入が完了しました。") 
