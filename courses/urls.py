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
from django.conf.urls.static import static
import courses.views
from djangoProject2 import settings
from questions import views
from courses import admin

urlpatterns = [


    path('list/', courses.views.CourseView.as_view()),
    path('purchase/', courses.views.purchase, name='course_purchase'),  # 购买课程
    path('detail/<int:course_id>/', courses.views.CourseDetail),
    path('revoke/', courses.views.revoke_course),
    path('republish/', courses.views.republish_course),
    path('download/video/<path:path>', courses.views.download_video, name='download_video'),
]

# 允许访问媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)