from django.urls import path

from . import views


app_name = 'question'

urlpatterns = [
    # All Questions
    path('', views.QuestionListView.as_view(), name='question_list'),
    # Search Page
    path('search/', views.question_search, name='question_search'),
    # Comment 
    path('add_comment/', views.add_comment, name='add_comment'),
    # Likes
    path('like/', views.like, name='question_like'),
    # Create / Update / Delete / Detail 
    path('create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('<slug:slug>/', views.question_detail, name='question_detail'),
    path('update/<slug:slug>/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('delete/<slug:slug>/', views.QuestionDeleteView.as_view(), name='question_delete'),
    # Category / User Questions
    path('user/<slug:slug>/', views.UserQuestionDetailView.as_view(), name='user_question_list'),
    path('category/<slug:slug>/', views.CategoryQuestionDetailView.as_view(), name='category_question_list'),
    ]
