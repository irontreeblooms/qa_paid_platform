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
from admin import views


urlpatterns = [

    path('questions/', views.AuditQuestionView.as_view()),  #问题审核
    path('answers/', views.AuditAnswerView.as_view()),      #回答审核
    path('courses/', views.AuditCourseView.as_view()),     #课程审核
    path('users/', views.ManageUserView.as_view()),        #用户管理
    path('appeals/', views.list_appeals, name='list_appeals'),  # 管理员查看申述
    path('appeals/<int:appeal_id>/', views.update_appeal_status, name='update_appeal_status'),  # 更新申述状态
]
