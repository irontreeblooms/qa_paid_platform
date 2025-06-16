from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True, verbose_name="昵称")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="头像")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="账户余额")
    bio = models.TextField(blank=True, null=True, verbose_name="个人简介")
    address = models.CharField(max_length=32, verbose_name="居住地")
    industry = models.CharField(max_length=16,verbose_name="所在行业")
    is_banned = models.BooleanField(default=False)
    # 性别选项（数据库存储值，显示名称）
    GENDER_CHOICES = (
        ('M', '男'),      # 存储 'M', 显示 '男'
        ('F', '女'),      # 存储 'F', 显示 '女'
        ('O', '其他'),    # 存储 'O', 显示 '其他'
        ('N', '保密'),    # 存储 'N', 显示 '保密'
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='N',        # 默认值为 'N'（保密）
        verbose_name='性别'
    )

class PurchaseRecord(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)  # 注意这里是字符串
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # 避免重复购买
