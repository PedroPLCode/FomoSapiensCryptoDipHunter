from django import template

register = template.Library()

@register.filter(name='startswith')
def startswith(value, arg):
    """
    Custom template filter to check if a string starts with a specified prefix.

    This filter is used in Django templates to check if the given string 
    (`value`) starts with the string passed as an argument (`arg`).

    Args:
        value (str): The string to check.
        arg (str): The prefix to check for.

    Returns:
        bool: True if the string starts with the specified prefix, False otherwise.
    """
    return value.startswith(arg)