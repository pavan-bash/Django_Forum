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
    path('<str:pk>/ask_question/', views.question_create, name='question_create'),
    path('login_question/<str:pk>', views.login_question, name='login_question'),
    path('upvote/<str:pk>/<str:pk1>', views.upvote, name='upvote'),
    path('downvote/<str:pk>/<str:pk1>', views.downvote, name='downvote'),
]