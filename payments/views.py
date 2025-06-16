from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from users.models import User
from .models import Transaction
import json
from decimal import Decimal

class TransactionView(View):
    """ 交易记录视图 """

    def get(self, request):
        """ 获取用户的交易记录 """
        user = request.user
        transactions = Transaction.objects.filter(user=user).order_by('-created_at')
        data = [
            {
                "id": t.id,
                "transaction_type": t.get_transaction_type_display(),
                "amount": str(t.amount),
                "created_at": t.created_at,
                "description": t.description
            } for t in transactions
        ]
        return JsonResponse({"transactions": data, "balance": user.balance}, safe=False)
