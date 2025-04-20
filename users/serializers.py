from rest_framework import serializers
from .models import User, PurchaseRecord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin']

class PurchasedCourseSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    price = serializers.DecimalField(source='course.price', max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = PurchaseRecord
        fields = ['id', 'course_title', 'price', 'created_at']