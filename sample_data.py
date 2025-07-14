import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from polls.models import Survey, Question, Choice, AnswerType

# 回答タイプを作成（既存があれば取得）
single_choice, _ = AnswerType.objects.get_or_create(name='single_choice')
multiple_choice, _ = AnswerType.objects.get_or_create(name='multiple_choice')
text_type, _ = AnswerType.objects.get_or_create(name='text')

# サーベイ（アンケート）を作成
survey = Survey.objects.create(
    title="AIの透明性・説明可能性・軽量化に関するアンケート",
    description="AI技術の社会的な受容や課題について、みなさまのご意見をお聞かせください。",
    pub_date=timezone.now()
)

# 1つ目の質問（単一選択・必須）
q1 = Question.objects.create(
    survey=survey,
    question_text="AIの透明性向上にどの程度関心がありますか？",
    pub_date=timezone.now(),
    answer_type=single_choice,
    is_required=True
)
for text in [
    "非常に関心がある",
    "やや関心がある",
    "どちらともいえない",
    "あまり関心がない",
    "全く関心がない"
]:
    Choice.objects.create(question=q1, choice_text=text, votes=0)

# 2つ目の質問（単一選択・必須）
q2 = Question.objects.create(
    survey=survey,
    question_text="AIがブラックボックスのままであることに不安を感じますか？",
    pub_date=timezone.now(),
    answer_type=single_choice,
    is_required=True
)
for text in [
    "感じる",
    "やや感じる",
    "どちらともいえない",
    "あまり感じない",
    "全く感じない"
]:
    Choice.objects.create(question=q2, choice_text=text, votes=0)

# 3つ目の質問（単一選択・必須）
q3 = Question.objects.create(
    survey=survey,
    question_text="計算資源を抑えたAI技術が社会に必要だと思いますか？",
    pub_date=timezone.now(),
    answer_type=single_choice,
    is_required=True
)
for text in [
    "強く思う",
    "やや思う",
    "どちらともいえない",
    "あまり思わない",
    "全く思わない"
]:
    Choice.objects.create(question=q3, choice_text=text, votes=0)

# 4つ目の質問（単一選択・必須）
q4 = Question.objects.create(
    survey=survey,
    question_text="説明可能なAIが普及することは、あなたの生活や仕事に役立つと感じますか？",
    pub_date=timezone.now(),
    answer_type=single_choice,
    is_required=True
)
for text in [
    "非常に役立つ",
    "やや役立つ",
    "どちらともいえない",
    "あまり役立たない",
    "全く役立たない"
]:
    Choice.objects.create(question=q4, choice_text=text, votes=0)

# 5つ目の質問（単一選択・必須）
q5 = Question.objects.create(
    survey=survey,
    question_text="AIの軽量化や環境負荷低減の取り組みについて、どの程度重要だと思いますか？",
    pub_date=timezone.now(),
    answer_type=single_choice,
    is_required=True
)
for text in [
    "非常に重要",
    "やや重要",
    "どちらともいえない",
    "あまり重要ではない",
    "全く重要ではない"
]:
    Choice.objects.create(question=q5, choice_text=text, votes=0)

# 7つ目の質問（複数選択・multiple_choiceの例）
q7 = Question.objects.create(
    survey=survey,
    question_text="AI技術に期待する分野をすべて選んでください（複数選択可）",
    pub_date=timezone.now(),
    answer_type=multiple_choice,
    is_required=False
)
for text in [
    "医療",
    "教育",
    "交通・物流",
    "製造業",
    "農業",
    "金融",
    "エンターテインメント",
    "その他"
]:
    Choice.objects.create(question=q7, choice_text=text, votes=0)


print("AIの透明性・説明可能性・軽量化に関するサンプルデータの投入が完了しました。") 
