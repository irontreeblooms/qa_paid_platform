import datetime
from django.contrib.sessions.models import Session
from django.utils.decorators import method_decorator
from django.views import View
import jwt
from questions.models import Question, Answer
from users.models import PurchaseRecord, User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


@csrf_exempt
def user_login(request):
    if request.method == "POST":

        data = json.loads(request.body)  # 解析 JSON 数据
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)  # 验证用户

        if user.is_banned:
            return JsonResponse({"error": "您已被封禁,请联系管理员解封"}, status=403)

        if user is not None:
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
    return JsonResponse(user_data)


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
        "status": c.course.status,
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
        }
        for q in questions
    ]

    return JsonResponse({'my_questions': question_list})


#发送验证码
@method_decorator(csrf_exempt, name='dispatch')
class SendCodeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"error": "无效的 JSON 数据"}, status=400)

        email = data.get("email")
        if not email:
            return JsonResponse({"error": "邮箱不能为空"}, status=400)

        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        cache.set(f'register_code_{email}', code, timeout=300)

        try:
            send_mail(
                subject="验证码通知",
                message=f"您的验证码是：{code}，5分钟内有效。",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )
            return JsonResponse({"message": "验证码发送成功"})
        except Exception as e:
            return JsonResponse({"error": "发送失败"}, status=500)


#注册用户
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"error": "无效的 JSON 数据"}, status=400)

        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        code = data.get("code")

        if not all([username, password, email, code]):
            return JsonResponse({"error": "请填写所有字段"}, status=400)

        cached_code = cache.get(f'register_code_{email}')
        if cached_code != code:
            return JsonResponse({"error": "验证码错误或已过期"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "用户名已存在"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "邮箱已注册"}, status=400)

        User.objects.create_user(username=username, email=email, password=password)
        cache.delete(f'register_code_{email}')
        return JsonResponse({"message": "注册成功"})


#查看用户的回答
@login_required
def my_answers(request):
    try:
        user = request.user
        # 获取用户的回答
        answers = Answer.objects.filter(user=user).select_related('question')

        # 获取所有相关问题的ID
        question_ids = answers.values_list('question', flat=True).distinct()
        questions = Question.objects.filter(id__in=question_ids)

        # 封装问题和对应的回答
        question_list = []
        for question in questions:
            # 获取该问题的所有回答
            related_answers = answers.filter(question=question)
            # 序列化问题及其回答
            question_list.append({
                'id': question.id,
                'title': question.title,
                'content': question.content,
                'reward': question.reward,
                'status': question.status,
                'user_id': user.id,
                'created_at': question.created_at.strftime('%Y-%m-%d %H:%M'),
                'answers': [
                    {
                        'id': answer.id,
                        'content': answer.content,
                        'status': answer.status,
                        'user':answer.user.username,
                        'created_at': answer.created_at.strftime('%Y-%m-%d %H:%M'),
                    }
                    for answer in related_answers
                ],
            })
        return JsonResponse({'myanswers_questions': question_list}, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def text(request):
    if request.method == "GET":
        created = 0
        skipped = 0
        for i in range(1, 101):
            username = f"testuser{i}"
            password = "123456"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password=password)  # 使用 create_user 自动加密密码
                created += 1
            else:
                skipped += 1
        return JsonResponse({
            "message": "批量用户创建完成",
            "created": created,
            "skipped": skipped
        }, status=200)
    else:
        return JsonResponse({"error": "仅支持 POST 请求"}, status=405)
