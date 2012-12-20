# -*- encoding: utf-8 -*-

from django.template import loader, RequestContext
from django.http import HttpResponseBadRequest

def bad_request(request,
                message,
                template='admin/bad_request.html',
                extra_context={}):
    extra_context['message'] = message
    rctx = RequestContext(request, extra_context)
    tpl = loader.get_template(template)
    return HttpResponseBadRequest(
        tpl.render(rctx))
