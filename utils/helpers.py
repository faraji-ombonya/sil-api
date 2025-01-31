from drf_spectacular.utils import OpenApiResponse, inline_serializer
from rest_framework import serializers


def get_paginated_response_schema(serializer_class, description):
    """
    Utility function to generate a paginated response schema for drf-spectacular.
    """
    return OpenApiResponse(
        response=inline_serializer(
            name=f"Paginated{serializer_class.__name__}Response",
            fields={
                "page": serializers.IntegerField(),
                "per_page": serializers.IntegerField(),
                "count": serializers.IntegerField(),
                "results": serializer_class(many=True),
            },
        ),
        description=description,
    )
