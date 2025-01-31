from rest_framework import serializers


class CustomPaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    count = serializers.IntegerField()
    results = serializers.ListSerializer(child=serializers.Serializer())
