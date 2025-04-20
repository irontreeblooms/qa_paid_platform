from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

@method_decorator(csrf_exempt, name='dispatch')
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
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=401)



@method_decorator(csrf_exempt, name='dispatch')
class QuestionDetailView(View):
    def get(self, request, pk ):
        """获取问题详情"""
        question = Question.objects.filter(pk=pk).first()
        data = QuestionSerializer(question).data
        return JsonResponse(data)

    def put(self, request, pk):
        """更新问题"""
        question = get_object_or_404(Question, pk=pk)
        data = json.loads(request.body)
        serializer = QuestionSerializer(question, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        """删除问题"""
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        return JsonResponse({'message': 'Question deleted'}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class AnswerView(View):
    def get(self, request, question_id):
        """获取某个问题下的所有回答"""
        answers = Answer.objects.filter(question_id=question_id, status='approved').order_by('-created_at')
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

        # 获取当前用户
        user = request.user  # 假设用户已认证

        # 在数据中填充问题ID和用户信息
        data['question'] = question.id
        data['user'] = user.id
        data['status'] = 'pending'  # 默认状态为待审核
        data['created_at'] = timezone.now()

        # 如果是收费回答，设置价格
        if 'is_paid' in data and data['is_paid']:
            if 'price' not in data or data['price'] <= 0:
                return JsonResponse({"error": "收费回答必须设置价格"}, status=400)

        # 序列化并保存回答
        serializer = AnswerSerializer(data=data)

        if serializer.is_valid():
            # 创建并保存回答
            answer = serializer.save()

            # 成功后返回创建的回答数据
            return JsonResponse(serializer.data, status=201)

        # 返回错误信息
        return JsonResponse(serializer.errors, status=400)
