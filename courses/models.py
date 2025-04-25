from django.db import models

# Create your models here.
from django.db import models
from users.models import User
class Course(models.Model):
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
        ('open', '开放'),
        ('closed', '关闭')
    ]

    title = models.CharField(max_length=255, verbose_name="课程标题")
    description = models.TextField(verbose_name="课程描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="课程价格")  # 0表示免费
    video = models.FileField(upload_to='videos/', verbose_name="课程视频", null=True, blank=True)  # 允许为空
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="上传者")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="审核状态")
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    def __str__(self):
        return self.title
