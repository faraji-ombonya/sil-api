from django.core.mail import mail_admins

from shop.models import Category


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


def send_email(subject: str, message: str):
    mail_admins(subject, message)
