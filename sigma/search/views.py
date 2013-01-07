from haystack.forms import SearchForm
from haystack.views import basic_search as haystack_basic_search


def basic_search(request):
    return haystack_basic_search(request, form_class=SearchForm)
