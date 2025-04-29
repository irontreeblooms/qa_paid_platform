from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    STATUS_CHOICES = [
        ('open', '开放中'),
        ('closed', '关闭显示'),
        ('pending', '审核中'),
        ('false', '审核失败'),
        ('answered', '已回答'),
    ]

    title = models.CharField(max_length=255)  # 标题
    content = models.TextField()              # 问题描述
    reward = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 悬赏金额
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # 问题状态
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)      # 更新时间

    # 提问者（与用户建立外键关系）
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')

    # 标签（多对多关系）
    tags = models.ManyToManyField(Tag, blank=True, related_name='questions')

    class Meta:
        ordering = ['-created_at']  # 默认按创建时间倒序排列

    def __str__(self):
        return self.title

# 2. 回答模型
class Answer(models.Model):
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '审核通过'),
        ('rejected', '审核未通过'),
        ('user_approved', '用户接受'),
        ('user_rejected', '用户拒绝'),
    ]
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()                 # 回答内容
    is_paid = models.BooleanField(default=False) # 是否为收费回答
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 回答价格（0表示免费）
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # 审核状态（待审核、通过、未通过）

    def __str__(self):
        return f'Answer by {self.user} on {self.question}'

    class Meta:
        ordering = ['-created_at']


# 3. 评论模型
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()                 # 评论内容
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.answer}'


# 4. 点赞模型
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')  # 防止同一用户对同一回答重复点赞

    def __str__(self):
        return f'{self.user} liked {self.answer}'


