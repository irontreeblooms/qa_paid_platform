from django.db import models

from users.models import User


class Transaction(models.Model):
    """ 交易记录模型 """
    TRANSACTION_TYPES = [
        ("deposit", "充值"),
        ("withdraw", "提现"),
        ("answer_income", "回答收入"),  # 用户因回答问题获得的赏金
        ("course_purchase", "购买课程"),  # 用户购买课程的支出
        ("course_income", "课程收入"),  # 用户上传的课程被购买后的收入
        ("question_reply", "问题支出"),  # 用户发布的问题的赏金支出
        ("other_income", "其它收入"),  # 其他收入
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 交易金额
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)  # 交易类型
    created_at = models.DateTimeField(auto_now_add=True)  # 交易时间
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username} - {self.get_transaction_type_display()} {self.amount} 元"

    class Meta:
        ordering = ['-created_at']  # 按交易时间倒序排序