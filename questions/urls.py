"""
URL configuration for djangoProject2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from questions import views
from courses import admin

urlpatterns = [

    path('question/list/', views.QuestionListView.as_view()),
    path('question/detail/<int:pk>/', views.QuestionDetailView.as_view()),
    path('question/answer/<int:question_id>/', views.AnswerView.as_view()),
    path('question/accept_answer/', views.accept_answer),
    path('question/reject_answer/', views.reject_answer),
    path('question/appeal/', views.create_appeal, name='create_appeal'),  # 提交申述
]
