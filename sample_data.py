import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from polls.models import Survey, Question, Choice

# サーベイ（アンケート）を作成
survey = Survey.objects.create(
    title="AIの透明性・説明可能性・軽量化に関するアンケート",
    description="AI技術の社会的な受容や課題について、みなさまのご意見をお聞かせください。",
    pub_date=timezone.now()
)  # type: ignore

# 1つ目の質問
q1 = Question.objects.create(
    survey=survey,
    question_text="AIの透明性向上にどの程度関心がありますか？",
    pub_date=timezone.now()
)  # type: ignore
for text in [
    "非常に関心がある",
    "やや関心がある",
    "どちらともいえない",
    "あまり関心がない",
    "全く関心がない"
]:
    Choice.objects.create(question=q1, choice_text=text, votes=0)  # type: ignore

# 2つ目の質問
q2 = Question.objects.create(
    survey=survey,
    question_text="AIがブラックボックスのままであることに不安を感じますか？",
    pub_date=timezone.now()
)  # type: ignore
for text in [
    "感じる",
    "やや感じる",
    "どちらともいえない",
    "あまり感じない",
    "全く感じない"
]:
    Choice.objects.create(question=q2, choice_text=text, votes=0)  # type: ignore

# 3つ目の質問
q3 = Question.objects.create(
    survey=survey,
    question_text="計算資源を抑えたAI技術が社会に必要だと思いますか？",
    pub_date=timezone.now()
)  # type: ignore
for text in [
    "強く思う",
    "やや思う",
    "どちらともいえない",
    "あまり思わない",
    "全く思わない"
]:
    Choice.objects.create(question=q3, choice_text=text, votes=0)  # type: ignore

# 4つ目の質問
q4 = Question.objects.create(
    survey=survey,
    question_text="説明可能なAIが普及することは、あなたの生活や仕事に役立つと感じますか？",
    pub_date=timezone.now()
)  # type: ignore
for text in [
    "非常に役立つ",
    "やや役立つ",
    "どちらともいえない",
    "あまり役立たない",
    "全く役立たない"
]:
    Choice.objects.create(question=q4, choice_text=text, votes=0)  # type: ignore

# 5つ目の質問
q5 = Question.objects.create(
    survey=survey,
    question_text="AIの軽量化や環境負荷低減の取り組みについて、どの程度重要だと思いますか？",
    pub_date=timezone.now()
)  # type: ignore
for text in [
    "非常に重要",
    "やや重要",
    "どちらともいえない",
    "あまり重要ではない",
    "全く重要ではない"
]:
    Choice.objects.create(question=q5, choice_text=text, votes=0)  # type: ignore

print("AIの透明性・説明可能性・軽量化に関するサンプルデータの投入が完了しました。") 
