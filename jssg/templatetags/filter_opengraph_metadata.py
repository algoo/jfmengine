from django import template

register = template.Library()

@register.filter
def filter_opengraph_metadata(metadata_dict_items):
  for key, value in metadata_dict_items:
    if key.startswith("og:"):
      yield (key, value)
