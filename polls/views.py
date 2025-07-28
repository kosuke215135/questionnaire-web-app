from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.detail import DetailView as DjangoDetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView as GenericDetailView, ListView
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Question, Choice, Survey, Answer, AnswerType, UserProfile
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from polls.utils.graph import plot_graph_with_path
import os
from django.utils import timezone
import uuid
import json
import re

# 認証関連のインポート
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django import forms

__all__ = ['DetailView', 'ResultsView', 'vote', 'SurveyDetailView', 'SurveyResultsView', 'survey_vote']

# Create your views here.

class DetailView(GenericDetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(GenericDetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, question.choice_set.model.DoesNotExist):
        # 選択肢が選ばれていない場合、エラーメッセージ付きで詳細ページを再表示
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': '選択肢を選んでください。',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # サーベイの集計結果ページへリダイレクト
        return redirect('polls:survey_results', pk=question.survey.pk)

class SurveyDetailView(DetailView):
    model = Survey
    template_name = 'polls/survey_detail.html'
    context_object_name = 'survey'

class SurveyResultsView(LoginRequiredMixin, DetailView):
    model = Survey
    template_name = 'polls/survey_results.html'
    context_object_name = 'survey'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.object
        results = []
        # グラフ画像保存先
        graph_dir = os.path.join('polls', 'static', 'polls', 'graph')
        os.makedirs(graph_dir, exist_ok=True)
        for question in survey.questions.all():
            colum = [choice.choice_text for choice in question.choices.all()]
            # Answerモデルを使って集計
            num = [Answer.objects.filter(question=question, choice=choice).count() for choice in question.choices.all()]
            pairs = list(zip(colum, num))
            # ファイル名例: survey1_q2.png
            filename = f'survey{survey.id}_q{question.id}.png'
            path = os.path.join(graph_dir, filename)
            # グラフ画像生成
            plot_graph_with_path(colum, num, path)
            # Webから参照するパス
            web_path = f'static/polls/graph/{filename}'
            results.append({
                "question": question,
                "colum": colum,
                "num": num,
                "pairs": pairs,
                "path": web_path,
            })
        context['results'] = results
        return context

class SurveyReviewView(DetailView):
    """投票内容の振り返りビュー"""
    model = Survey
    template_name = 'polls/survey_review.html'
    context_object_name = 'survey'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.object
        user_answers = []
        
        # ユーザーの最新の回答を取得
        for question in survey.questions.all():
            if question.answer_type.name == 'single_choice':
                # 単一選択の場合 - 最新の回答のみ
                latest_answer = Answer.objects.filter(
                    question=question,
                    user=self.request.user if self.request.user.is_authenticated else None
                ).order_by('-submitted_at').first()
                
                if latest_answer and latest_answer.choice:
                    user_answers.append({
                        'question': question,
                        'answers': [latest_answer.choice.choice_text],
                        'type': 'choice'
                    })
                else:
                    user_answers.append({
                        'question': question,
                        'answers': [],
                        'type': 'choice'
                    })
            elif question.answer_type.name == 'multiple_choice':
                # 複数選択の場合 - 最新の投票セッション内のすべての選択肢
                # 最新の回答時刻を取得（1秒以内の誤差を許容）
                latest_answers = Answer.objects.filter(
                    question=question,
                    user=self.request.user if self.request.user.is_authenticated else None
                ).order_by('-submitted_at')
                
                if latest_answers.exists():
                    latest_time = latest_answers.first().submitted_at
                    # 最新時刻から1秒以内の回答をすべて取得
                    from datetime import timedelta
                    recent_answers = Answer.objects.filter(
                        question=question,
                        user=self.request.user if self.request.user.is_authenticated else None,
                        submitted_at__gte=latest_time - timedelta(seconds=1),
                        submitted_at__lte=latest_time + timedelta(seconds=1)
                    ).select_related('choice')
                    
                    choices = [answer.choice.choice_text for answer in recent_answers if answer.choice]
                    # 重複を除去してユニークな選択肢のみを表示
                    unique_choices = list(dict.fromkeys(choices))
                    user_answers.append({
                        'question': question,
                        'answers': unique_choices,
                        'type': 'choice'
                    })
                else:
                    user_answers.append({
                        'question': question,
                        'answers': [],
                        'type': 'choice'
                    })
            elif question.answer_type.name == 'text':
                # 記述式の場合 - 最新の回答のみ
                latest_answer = Answer.objects.filter(
                    question=question,
                    user=self.request.user if self.request.user.is_authenticated else None
                ).order_by('-submitted_at').first()
                
                if latest_answer and latest_answer.text.strip():
                    user_answers.append({
                        'question': question,
                        'answers': [latest_answer.text.strip()],
                        'type': 'text'
                    })
                else:
                    user_answers.append({
                        'question': question,
                        'answers': [],
                        'type': 'text'
                    })
        
        context['user_answers'] = user_answers
        return context

def survey_vote(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        for question in survey.questions.all():
            # 単一選択設問
            if question.answer_type.name == 'single_choice':
                choice_id = request.POST.get(f'question_{question.id}')
                if choice_id:
                    try:
                        selected_choice = Choice.objects.get(pk=choice_id, question=question)
                        # Answerモデルに新規保存（毎回新規で記録）
                        Answer.objects.create(
                            question=question,
                            user=user,
                            choice=selected_choice,
                            text='',
                        )
                    except Choice.DoesNotExist:
                        pass  # 不正な選択肢IDは無視
            # 複数選択設問
            elif question.answer_type.name == 'multiple_choice':
                choice_ids = request.POST.getlist(f'question_{question.id}')
                for choice_id in choice_ids:
                    try:
                        selected_choice = Choice.objects.get(pk=choice_id, question=question)
                        Answer.objects.create(
                            question=question,
                            user=user,
                            choice=selected_choice,
                            text='',
                        )
                    except Choice.DoesNotExist:
                        pass
            # 記述式設問
            elif question.answer_type.name == 'text':
                text_value = request.POST.get(f'question_{question.id}', '').strip()
                if text_value:
                    Answer.objects.create(
                        question=question,
                        user=user,
                        choice=None,
                        text=text_value,
                    )
        return redirect('polls:survey_review', pk=survey.pk)
    else:
        return redirect('polls:survey_detail', pk=survey.pk)

def question_cell(request):
    unique_id = uuid.uuid4().hex
    html = render_to_string('polls/partials/question_cell.html', {'unique_id': unique_id})
    return HttpResponse(html)

def survey_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        survey = Survey.objects.create(
            title=title, 
            description=description, 
            pub_date=timezone.now(),
            created_by=request.user if request.user.is_authenticated else None
        )
        question_texts = request.POST.getlist('question_text')
        # ユニークIDを抽出
        question_ids = []
        for key in request.POST.keys():
            m = re.match(r'question_type_(.+)', key)
            if m:
                question_ids.append(m.group(1))
        question_types = []
        choices_per_question = []
        for qid in question_ids:
            question_types.append(request.POST.get(f'question_type_{qid}'))
            choices_per_question.append(request.POST.getlist(f'choice_text_{qid}'))
        is_requireds = request.POST.getlist('is_required')
        type_map = {
            'single': 'single_choice',
            'multiple': 'multiple_choice',
            'text': 'text'
        }
        for i, (q_text, q_type) in enumerate(zip(question_texts, question_types)):
            answer_type_name = type_map.get(q_type, 'single_choice')
            answer_type = AnswerType.objects.get(name=answer_type_name)
            is_required = str(i) in is_requireds or True  # 必須チェック（暫定）
            question = Question.objects.create(
                survey=survey,
                question_text=q_text,
                answer_type=answer_type,
                is_required=is_required,
                pub_date=timezone.now()
            )
            # 選択肢を保存
            if q_type in ['single', 'multiple']:
                if i < len(choices_per_question):
                    for c_text in choices_per_question[i]:
                        if c_text:
                            Choice.objects.create(question=question, choice_text=c_text)
        return redirect('polls:survey_list')
    return render(request, 'polls/survey_create.html')

# 認証関連のフォーム
class CustomUserCreationForm(UserCreationForm):
    """カスタムユーザー登録フォーム"""
    email = forms.EmailField(required=True, help_text='必須項目です')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    """ユーザープロフィール編集フォーム"""
    class Meta:
        model = UserProfile
        fields = ('bio', 'birth_date')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 認証関連のビュー
class SignUpView(CreateView):
    """ユーザー登録ビュー"""
    form_class = CustomUserCreationForm
    template_name = 'polls/signup.html'
    success_url = '/polls/survey_list/'

    def form_valid(self, form):
        response = super().form_valid(form)
        # 登録後自動ログイン
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'アカウントが正常に作成されました！')
        return response

class LoginView(View):
    """ログインビュー"""
    template_name = 'polls/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('polls:survey_list')
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'ようこそ、{username}さん！')
                return redirect('polls:survey_list')
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    """ログアウトビュー"""
    def get(self, request):
        logout(request)
        messages.info(request, 'ログアウトしました。')
        return redirect('polls:login')

class ProfileView(LoginRequiredMixin, UpdateView):
    """プロフィール編集ビュー"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'polls/profile.html'
    success_url = '/polls/profile/'

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'プロフィールが更新されました！')
        return super().form_valid(form)

class SurveyListView(ListView):
    """アンケート一覧ビュー"""
    model = Survey
    template_name = 'polls/survey_list.html'
    context_object_name = 'surveys'
    ordering = ['-pub_date']

    def get_queryset(self):
        """ログイン状態に応じてアンケートを取得"""
        if self.request.user.is_authenticated:
            # ログインユーザーは自分のアンケートのみ表示
            return Survey.objects.filter(created_by=self.request.user)
        else:
            # 未ログインユーザーはすべてのアンケートを表示
            return Survey.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
