from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('community/', views.community, name='community'),
    path('popular/', views.all_questions, name='all_questions'),
    path('my_communities/', views.my_communities, name='my_communities'),
    path('community/<str:pk>', views.community_detail, name='community_detail'),    
    path('community/create/', views.community_create, name='community_create'),
    path('question/<str:pk>', views.question_detail, name='question_detail'),
    path('question/<str:pk>/reply/<str:pk1>', views.question_detail_reply, name='question_detail_reply'),
    path('<str:pk>/question/create', views.question_create, name='question_create'),
    path('question/edit/<str:pk>', views.question_edit, name='question_edit'),
    path('answer/edit/<str:pk>', views.answer_edit, name='answer_edit'),
    path('login_question/<str:pk>', views.login_question, name='login_question'),
    path('reportqtest/<str:pk>', views.reportqtest, name='reportqtest'),
    path('reportq/<str:pk>', views.reportq, name='reportq'),
    path('reportatest/<str:pk>', views.reportatest, name='reportatest'),
    path('reporta/<str:pk>', views.reporta, name='reporta'),
    path('tag/<str:pk>', views.tag_detail, name='tag_detail'),
    path('like_answer/', views.like_answer, name='like_answer'),
]