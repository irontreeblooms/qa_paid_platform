from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Question, Answer, Appeal
from .serializers import QuestionSerializer, AnswerSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import F
from users.models import User
from payments.models import Transaction
from django.db.models import Q

class QuestionListView(View):
    def get(self, request):
        """获取问题列表（支持分页 + 搜索）"""
        search = request.GET.get('search', '')
        page = request.GET.get('page', 1)
        from django.db.models import Q

        # 查询
        questions = Question.objects.filter(
            Q(title__icontains=search) & (Q(status='open') | Q(status='answered'))
        ).order_by('-created_at')

        paginator = Paginator(questions, 10)  # 每页10条
        page_obj = paginator.get_page(page)

        data = QuestionSerializer(page_obj, many=True).data
        return JsonResponse({
            'questions': data,
            'count': paginator.count,
            'num_pages': paginator.num_pages
        })

    def post(self, request):
        """创建问题"""
        data = json.loads(request.body)
        data['user'] = request.user.id
        serializer = QuestionSerializer(data=data)

        if serializer.is_valid() and request.user.is_authenticated:
            print(data)
            user = User.objects.filter(id=data['user']).first()
            if user.balance >= data['reward']:
                User.objects.filter(id=data['user']).update(balance=F('balance') - data['reward'])
                # 创建交易记录

                Transaction.objects.create(
                    user_id=data['user'],
                    transaction_type="question_reply",
                    amount=data['reward'],
                    description=f"发布问题（标题: {data['title']}）支付",
                    created_at=now()
                )
            else:
                return JsonResponse({'error': '该用户余额不足'}, status=400)
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=401)



class QuestionDetailView(View):
    def get(self, request, pk):
        """获取问题详情"""
        question = get_object_or_404(Question, pk=pk)
        data = QuestionSerializer(question).data
        return JsonResponse(data)

    def put(self, request, pk):
        """更新问题"""
        question = get_object_or_404(Question, pk=pk)

        # 权限校验
        if question.user != request.user:
            return JsonResponse({'error': ('无权限更新该问题')}, status=403)

        data = json.loads(request.body)
        serializer = QuestionSerializer(question, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        """删除问题"""
        question = get_object_or_404(Question, pk=pk)

        # 权限校验，确保只有创建者能删除该问题
        if question.status == "pending":
            return JsonResponse({'error': '请先撤销发布该问题后再删除'}, status=403)

        question.delete()
        return JsonResponse({'message': '问题已成功删除'}, status=204)



class AnswerView(View):
    def get(self, request, question_id):
        """获取某个问题下的所有回答"""
        answers = Answer.objects.filter(
            question_id=question_id
        ).exclude(
            Q(status='pending') | Q(status='rejected')
        ).order_by('-created_at')
        data = AnswerSerializer(answers, many=True).data
        return JsonResponse(data, safe=False)

    def post(self, request, question_id):
        """创建回答"""
        # 解析请求数据
        data = json.loads(request.body)

        try:
            # 检查问题是否存在
            question = Question.objects.get(id=question_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "问题不存在"}, status=404)

        answer = Answer.objects.filter(user=request.user, question=question_id)
        if answer.exists():  # 检查 QuerySet 是否有结果
            return JsonResponse({"error": "您已回答过该问题"}, status=200)

        # 获取当前用户
        user = request.user  # 假设用户已认证

        # 在数据中填充问题ID和用户信息
        data['question'] = question.id
        data['user'] = user.id
        data['status'] = 'pending'  # 默认状态为待审核
        data['created_at'] = timezone.now()


        # 序列化并保存回答
        serializer = AnswerSerializer(data=data)

        if serializer.is_valid():
            # 创建并保存回答
            answer = serializer.save()

            # 成功后返回创建的回答数据
            return JsonResponse(serializer.data, status=201)

        # 返回错误信息
        return JsonResponse(serializer.errors, status=400)



def accept_answer(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            answer_id = body.get('answer_id')
            if not answer_id:
                return JsonResponse({'error': 'Answer ID is required'}, status=400)

            # 获取回答对象
            answer = get_object_or_404(Answer, id=answer_id)

            if answer.status == 'user_rejected':
                return JsonResponse({'message': 'Answer has been rejected by user'}, status=403)

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

            answer.save()

            return JsonResponse({'message': 'Answer has been accepted'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



def reject_answer(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            answer_id = body.get('answer_id')
            if not answer_id:
                return JsonResponse({'error': 'Answer ID is required'}, status=400)
            # 获取回答对象
            answer = get_object_or_404(Answer, id=answer_id)
            if answer.status == 'user_approved':
                return JsonResponse({'message': 'Answer has been approved by user'}, status=403)

            # 更新回答状态为 "rejected"
            answer.status = 'user_rejected'
            answer.save()

            return JsonResponse({'message': 'Answer has been rejected'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)




def create_appeal(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            question_id = data.get('question_id')
            answer_id = data.get('answer_id')
            reason = data.get('reason')

            if not reason:
                return JsonResponse({'error': '申述理由不能为空'}, status=400)

            question = get_object_or_404(Question, id=question_id) if question_id else None
            answer = get_object_or_404(Answer, id=answer_id) if answer_id else None

            appeal = Appeal.objects.create(
                user=user,
                question=question,
                answer=answer,
                reason=reason
            )
            return JsonResponse({'message': '申述已提交', 'appeal_id': appeal.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': '请求格式错误'}, status=400)
    else:
        return JsonResponse({'error': '仅支持 POST 请求'}, status=405)