import datetime
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django import forms
from django.views import View
import jwt

from payments.models import Transaction
from questions.models import Question
from users import models
from users.models import User, PurchaseRecord
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from users.models import User
import json

from users.serializers import PurchasedCourseSerializer


@csrf_exempt
def user_login(request):

    if request.method == "POST":
        data = json.loads(request.body)  # 解析 JSON 数据
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)  # 验证用户
        if user is not None:
            print(user.is_superuser)
            login(request, user)  # 登录用户

            return JsonResponse({'code': 200, 'info': '登陆成功'})
        else:
            return JsonResponse({"error": "用户名或密码错误"}, status=400)

    return JsonResponse({"error": "仅支持 POST 请求"}, status=405)

@csrf_exempt
def Admin_login(request):
    if request.method == "OPTIONS":
        # 处理 CORS 预检请求
        response = JsonResponse({"message": "CORS preflight successful"})
        response["Access-Control-Allow-Origin"] = "http://localhost:8080"  # 允许的前端地址
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

    if request.method == "POST":
        data = json.loads(request.body)  # 解析 JSON 数据
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)  # 验证用户
        if user is not None:
            login(request, user)  # 登录用户

            return JsonResponse({'code': 200, 'info': '登陆成功'})
        else:
            return JsonResponse({"error": "用户名或密码错误"}, status=400)

    return JsonResponse({"error": "仅支持 POST 请求"}, status=405)



@csrf_exempt
@login_required
def logout(request):
    if request.method == "POST":
        sessionid = request.COOKIES.get('sessionid')  # 获取当前请求的 sessionid
        response = HttpResponse("Logout successful")
        response.delete_cookie(sessionid)  # 删除cookie
        try:
            session_key = request.session.session_key
            if session_key:
                session = Session.objects.get(session_key=session_key)
                session.delete()  # 删除数据库中的 session
        except Session.DoesNotExist:
            pass  # 如果 session 不存在，也可以安全地跳过
        return response

# 获取当前用户信息
@login_required
def user_detail(request):
    user = request.user  # 获取当前登录的用户
    user_data = {
        "id": user.id,
        "nickname": user.nickname,
        "bio": user.bio,
        "address": user.address,
        "industry": user.industry,
        "gender": user.gender
    }
    1(user_data)


# 通用修改用户信息的 API
@csrf_exempt
@login_required
def edit_user_info(request):
    """ 修改用户信息（支持昵称、简介、地址、行业、性别） """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

    data = json.loads(request.body)
    user = request.user  # 获取当前登录用户

    fields_to_update = ["nickname", "bio", "address", "industry", "gender"]
    for field in fields_to_update:
        if field in data:
            setattr(user, field, data[field])  # 更新字段

    user.save()
    return JsonResponse({"message": "Profile updated successfully", "user": {
        "nickname": user.nickname,
        "bio": user.bio,
        "address": user.address,
        "industry": user.industry,
        "gender": user.gender
    }})


#查看用户购买的课程
@login_required
def purchased_courses(request):
    user = request.user
    purchases = PurchaseRecord.objects.filter(user=user).select_related('course')

    data = [{
        "id": c.course.id,
        "title": c.course.title,
        "description": c.course.description,
        "price": str(c.course.price),
        "video": c.course.video.url if c.course.video else None,
        "cover": c.course.cover.url if c.course.cover else None,
    } for c in purchases]

    return JsonResponse({'purchased_courses': data})


#查看用户发布的问题
@login_required
def my_questions(request):
    user = request.user
    questions = Question.objects.filter(user=user)

    question_list = [
        {
            'id': q.id,
            'title': q.title,
            'content': q.content,
            'reward': q.reward,
            'status': q.status,
            'user_id': user.id,
            'created_at': q.created_at.strftime('%Y-%m-%d %H:%M'),
            # 添加更多字段视需要而定
        }
        for q in questions
    ]

    return JsonResponse({'my_questions': question_list})


def JwtTest(request):
    headers = {
        'alg': 'HS256',
        'typ': 'JWT'
    }  # jwt的头部，包含了类型和算法的指定

    payload = {
        "id": 123,
        "username": '小明',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12),
    }  # jwt的负载，都是一些自定义值,其中exp中的内容是我们指定jwt的一个有效时间，有效时间为12个小时

    token = jwt.encode(headers=headers, payload=payload, algorithm='HS256', key='123')  # 对上面内容进行加密，这里的key就是加的盐
    print(token)
    return redirect("http://127.0.0.1:8000/api/users/user/detail")