from django import template

register = template.Library()


@register.filter
def has_group(user, group_name):
    """
    Check whether the logged-in user belongs to a specific
    dashboard manager group.

    Superusers automatically have access to everything.
    """

    if not user or not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return user.groups.filter(name=group_name).exists()