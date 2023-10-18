from rest_framework import serializers


class TodoInputSerializer(serializers.Serializer):
    task = serializers.CharField(required=False, max_length=100)
    completed = serializers.BooleanField(required=False)
