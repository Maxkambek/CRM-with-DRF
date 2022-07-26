from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            'id',
            'owner',
            'title',
            'description',
            'deadline',
            'status',
            'priority',
            'created_at'
        ]
        extra_kwargs = {
            'owner': {
                'required': False
            }
        }
