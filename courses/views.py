import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from .models import Course
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from users.models import User, PurchaseRecord
from payments.models import Transaction
from django.db.models import F
from courses.serializers import CourseSerializer
from django.core.paginator import Paginator
from django.db.models import Q

@method_decorator(csrf_exempt, name='dispatch')
class CourseView(View):
    def get(self, request):
        """获取课程列表（支持分页 + 搜索）"""

        # 获取搜索参数和页码
        search = request.GET.get('search', '')  # 获取搜索参数
        try:
            page = int(request.GET.get('page', 1))  # 获取当前页码，默认为1
        except ValueError:
            return JsonResponse({'error': 'Invalid page number'}, status=400)

        # 查询课程，支持模糊搜索课程标题和描述，并且只查询审核通过的课程
        courses = Course.objects.filter(
            Q(title__icontains=search) | Q(description__icontains=search),  # 模糊搜索标题和描述
            status='approved'  # 只查询审核通过的课程
        ).order_by('-created_at')  # 按创建时间倒序排列

        # 分页功能
        paginator = Paginator(courses, 12)
        page_obj = paginator.get_page(page)  # 获取当前页的数据

        # 使用序列化器来序列化课程数据
        data = CourseSerializer(page_obj, many=True).data

        return JsonResponse({
            'courses': data,  # 返回序列化后的课程数据
            'count': paginator.count,  # 总记录数
            'num_pages': paginator.num_pages,  # 总页数
            'current_page': page_obj.number  # 当前页码
        })

    def post(self, request):
        """上传课程"""
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price', 0.00)
        video = request.FILES.get('video')
        cover = request.FILES.get("cover")

        if not video:
            return JsonResponse({"error": "请上传视频文件"}, status=400)

        course = Course.objects.create(title=title, description=description, price=price, video=video, author=request.user,cover=cover)
        return JsonResponse({"message": "上传成功", "course_id": course.id, "video_url": course.video.url}, status=201)


@csrf_exempt
def purchase(request):
    """购买课程"""
    try:
        data = json.loads(request.body)
        course_id = data.get("course_id")
        user = request.user
        user_id = user.id
        course = Course.objects.get(id=course_id)

        #向用户已购课程中添加课程

        # 检查是否已购买
        if PurchaseRecord.objects.filter(user=user, course=course).exists():
            return JsonResponse({'status': 'already_purchased'}, status=400)
        else:
            PurchaseRecord.objects.create(user=user, course=course)


        # 检查用户余额是否足够
        if user.balance < course.price:
            return JsonResponse({"error": "余额不足"}, status=400)

        # 扣除用户余额
        User.objects.filter(id=user_id).update(balance=F('balance') - course.price)

        # 给作者增加收入
        User.objects.filter(id=course.author_id).update(balance=F('balance') + course.price)

        # 记录交易：用户购买课程
        Transaction.objects.create(
            user=user,
            transaction_type="course_purchase",
            amount=-course.price,
            description=f"购买课程《{course.title}》",
        )

        # 记录交易：作者获得课程收入
        Transaction.objects.create(
            user=course.author,
            transaction_type="course_income",
            amount=course.price,
            description=f"课程《{course.title}》被购买",
        )

        return JsonResponse({"message": "购买成功", "course_id": course.id})

    except Course.DoesNotExist:
        return JsonResponse({"error": "课程不存在"}, status=404)
    except User.DoesNotExist:
        return JsonResponse({"error": "用户不存在"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def CourseDetail(request,course_id):
    course = Course.objects.filter(id = course_id)
    data = CourseSerializer(course, many=True).data
    print(data)
    print("sha")
    return JsonResponse(data, safe=False)