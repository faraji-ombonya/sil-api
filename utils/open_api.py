from drf_spectacular.utils import (
    OpenApiResponse,
    OpenApiParameter,
    inline_serializer,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers


def get_paginated_response_schema(
    serializer_class: serializers.ModelSerializer, description: str
) -> OpenApiResponse:
    """
    Utility function to generate a paginated response schema for
    drf-spectacular.
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


page = OpenApiParameter(
    name="page",
    type=OpenApiTypes.INT,
    location=OpenApiParameter.QUERY,
    description="Page number",
    default=1,
    required=False,
)


per_page = OpenApiParameter(
    name="per_page",
    type=OpenApiTypes.INT,
    location=OpenApiParameter.QUERY,
    description="Number of items per page",
    default=10,
    required=False,
)
