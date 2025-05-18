from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
import users.models
from questions.models import Question, Answer, Appeal
from courses.models import Course
from users.models import User
from questions.serializers import QuestionSerializer, AnswerSerializer
from users.serializers import UserSerializer
from courses.serializers import CourseSerializer
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from payments.models import Transaction

# 管理员权限检查
def is_admin(user):
    return user.is_authenticated and user.is_admin

@method_decorator(csrf_exempt, name='dispatch')
class AuditQuestionView(View):
    """审核问题"""

    def get(self, request):
        """获取所有待审核的问题"""
        questions = Question.objects.filter(status='pending')
        serializer = QuestionSerializer(questions, many=True)
        return JsonResponse({'questions': serializer.data}, safe=False)

    def post(self, request):
        """审核通过或拒绝问题"""
        try:
            data = json.loads(request.body)  # 解析 JSON 数据
            question_id = data.get('question_id')
            new_status = data.get('status')
        except json.JSONDecodeError:
            return JsonResponse({'error': '请求体格式错误'}, status=400)

        if not question_id:
            return JsonResponse({'error': 'question_id 不能为空'}, status=400)

        question = get_object_or_404(Question, id=question_id)

        if new_status == "false":
            #审核不通过退余额
            User.objects.filter(id=question.user_id).update(balance=F('balance') + question.reward)
            # 创建交易记录
            Transaction.objects.create(
                user_id=question.user_id,
                transaction_type="other_income",
                amount=question.reward,
                description=f"发布问题（ID: {question.id}）失败",
                created_at=now()
            )

        valid_statuses = dict(Question.STATUS_CHOICES).keys()

        if new_status not in valid_statuses:
            return JsonResponse({'error': '非法状态值'}, status=400)

        question.status = new_status
        question.save()
        return JsonResponse({'message': '审核成功', 'status': question.status}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AuditAnswerView(View):
    """审核回答"""

    def get(self, request):
        """获取所有待审核的回答"""
        answers = Answer.objects.filter(status='pending')
        serializer = AnswerSerializer(answers, many=True)
        return JsonResponse({'answers': serializer.data}, status=200)

    def post(self, request):
        """审核回答（通过/拒绝）"""
        try:
            data = json.loads(request.body)
            answer_id = data.get('answer_id')
            new_status = data.get('status')
            # 确保 `status` 是合法的选项
            valid_statuses = dict(Answer.STATUS_CHOICES).keys()
            if new_status not in valid_statuses:
                return JsonResponse({'error': '非法状态值'}, status=400)
            answer = get_object_or_404(Answer, id=answer_id)
            answer.status = new_status
            answer.save()

            return JsonResponse({'message': '审核成功', 'status': answer.status}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': '请求格式错误'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class AuditCourseView(View):
    """审核课程"""
    def get(self, request):
        """获取所有待审核的课程"""
        courses = Course.objects.filter(status='pending')
        serializer = CourseSerializer(courses, many=True)
        return JsonResponse({'courses': serializer.data}, status=200)

    def post(self, request):
        """审核通过或拒绝课程"""
        try:
            data = json.loads(request.body)
            course_id = data.get('course_id')
            new_status = data.get('status')

            # 确保 `status` 是合法的选项
            valid_statuses = dict(Course.STATUS_CHOICES).keys()
            if new_status not in valid_statuses:
                return JsonResponse({'error': '非法状态值'}, status=400)
            course = get_object_or_404(Course, id=course_id)
            course.status = new_status
            course.save()

            return JsonResponse({'message': '审核成功', 'status': course.status}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': '请求格式错误'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ManageUserView(View):
    """管理用户"""
    def get(self, request):
        users = User.objects.all()
        data = UserSerializer(users, many=True).data
        return JsonResponse({'users': data})

    def post(self, request):
        """更新用户状态"""
        data = json.loads(request.body)

        try:
            user = User.objects.get(id=data['user_id'])
            if 'is_superuser' in data:
                user.is_superuser = data['is_superuser']
            if 'is_banned' in data:
                user.is_banned = data['is_banned']
            user.save()
            return JsonResponse({'message': '用户状态更新成功'})
        except User.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



@csrf_exempt
def list_appeals(request):
    if request.method == 'GET':
        appeals = Appeal.objects.all().order_by('-created_at')
        appeals_data = [
            {
                'id': appeal.id,
                'user': appeal.user.username,
                'question': appeal.question.title if appeal.question else None,
                'answer': appeal.answer.content if appeal.answer else None,
                'reason': appeal.reason,
                'status': appeal.status,
                'created_at': appeal.created_at,
                'updated_at': appeal.updated_at,
            }
            for appeal in appeals
        ]
        return JsonResponse({'appeals': appeals_data}, safe=False)
    else:
        return JsonResponse({'error': '仅支持 GET 请求'}, status=405)


@csrf_exempt
def update_appeal_status(request, appeal_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            answer_id = data.get('answer_id')
            appeal = get_object_or_404(Appeal, id=appeal_id)

            if new_status not in dict(Appeal.STATUS_CHOICES):
                return JsonResponse({'error': '无效的状态值'}, status=400)

            if new_status=='resolved':
                # 获取回答对象
                answer = get_object_or_404(Answer,user=appeal.user,question = appeal.question)
                # 更新回答状态为 "user_approved"
                answer.status = 'user_approved'
                # 将奖励给予问题的回答者
                question = Question.objects.filter(id=answer.question_id).first()
                User.objects.filter(id=answer.user_id).update(balance=F('balance') + question.reward)

                # 创建交易记录
                from payments.models import Transaction
                Transaction.objects.create(
                    user_id=answer.user_id,
                    transaction_type="answer_income",
                    amount=question.reward,
                    description=f"回答问题（ID: {question.id}）获得奖励",
                    created_at=now()
                )

            appeal.status = new_status
            appeal.save()

            return JsonResponse({'message': '申述状态已更新', 'status': appeal.status}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': '请求格式错误'}, status=400)
    else:
        return JsonResponse({'error': '仅支持 PUT 请求'}, status=405)