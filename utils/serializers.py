from rest_framework import serializers


class GenericPaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    count = serializers.IntegerField()
    results = serializers.SerializerMethodField()

    def get_results(self, obj):
        """
        Dynamically determine the child serializer based on the context.
        """
        serializer_class = self.context.get("child_serializer")
        if not serializer_class:
            raise ValueError("child_serializer must be provided in context")
        return serializer_class(obj, many=True).data
