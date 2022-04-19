from django import template
from ..forms import SearchForm


register = template.Library()


@register.inclusion_tag('../templates/partials/search.html')
def search_box():
    context = {
        'search_box': SearchForm,
    }
    return context

