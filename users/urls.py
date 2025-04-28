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
from users import views
from courses import admin

urlpatterns = [

    #用户信息
    path('user/detail/', views.user_detail),
    path('user/edit/', views.edit_user_info),
    path('user/login/', views.user_login, name='user_login'),
    path('admin/login/', views.Admin_login, name='admin_login'),
    path('user/logout/', views.logout, name='user_logout'),
    path('user/my-courses/', views.purchased_courses, name='my_courses'),
    path('user/my-questions/', views.my_questions, name='my_questions'),
    path('send-code/', views.SendCodeView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('myanswers/', views.my_answers),
]
