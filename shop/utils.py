from .models import Category


def get_descendant_categories(category):
    """Recursively fetch all descendant categories of a given category."""
    descendants = []
    children = Category.objects.filter(parent=category)
    for child in children:
        descendants.append(child)
        descendants.extend(get_descendant_categories(child))
    return descendants
