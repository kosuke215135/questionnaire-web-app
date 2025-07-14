import os
import django
import random
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from polls.models import Survey, Question, Choice, Answer, AnswerType

# ダミー記述式回答例
DUMMY_TEXTS = [
    "とても良いと思います。",
    "改善の余地があると感じます。",
    "特にありません。",
    "AIの発展に期待しています。",
    "使いやすいサービスを希望します。",
    "セキュリティ面が心配です。",
    "もっと多様な機能が欲しいです。",
    "サポートが充実していると嬉しいです。",
    "操作が直感的で助かります。",
    "今後も利用したいです。"
]

for survey in Survey.objects.all():
    for question in survey.questions.all():
        if question.answer_type.name == 'single_choice':
            choices = list(question.choices.all())
            for _ in range(20):
                if choices:
                    selected = random.choice(choices)
                    Answer.objects.create(
                        question=question,
                        user=None,
                        choice=selected,
                        text='',
                    )
        elif question.answer_type.name == 'multiple_choice':
            choices = list(question.choices.all())
            for _ in range(20):
                if choices:
                    selected_choices = random.sample(choices, k=min(len(choices), random.randint(2, 3)))
                    for selected in selected_choices:
                        Answer.objects.create(
                            question=question,
                            user=None,
                            choice=selected,
                            text='',
                        )
        elif question.answer_type.name == 'text':
            for _ in range(20):
                Answer.objects.create(
                    question=question,
                    user=None,
                    choice=None,
                    text=random.choice(DUMMY_TEXTS),
                )

print("ダミー回答データの投入が完了しました。") 