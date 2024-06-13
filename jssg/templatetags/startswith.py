from django import template

register = template.Library()

@register.tag
def is_opengraph(text):
    if isinstance(text, str) and text.startswith("og:"):
        return True
    return False

@register.tag
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False