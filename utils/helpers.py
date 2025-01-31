from drf_spectacular.utils import OpenApiResponse, inline_serializer
from rest_framework import serializers

from shop.models import Category


def get_paginated_response_schema(
    serializer_class: serializers.ModelSerializer, description: str
) -> OpenApiResponse:
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


def get_category_tree(category: Category) -> list[Category]:
    """Utility function to get the category tree.

    Args:
        category (Category): The category to get the tree for.

    Returns:
        list: The category tree.
    """
    visited = set()
    categories = []
    while category:
        if category.id in visited:
            break
        visited.add(category.id)
        categories.append(category)
        category = category.parent
    categories.reverse()
    return categories
