from django.urls import path
from . import views
from .views import SurveyDetailView, SurveyResultsView, survey_vote


urlpatterns = [
    # 認証関連のURL
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    
    # アンケート一覧
    path('survey_list/', views.SurveyListView.as_view(), name='survey_list'),
    
    # 既存のURL
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('survey/<int:pk>/', SurveyDetailView.as_view(), name='survey_detail'),
    path('survey/<int:pk>/results/', SurveyResultsView.as_view(), name='survey_results'),
    path('survey/<int:pk>/review/', views.SurveyReviewView.as_view(), name='survey_review'),
    path('survey/<int:pk>/vote/', survey_vote, name='survey_vote'),
    path('survey/create/', views.survey_create, name='survey_create'),
    path('survey/question_cell/', views.question_cell, name='question_cell'),
] 
