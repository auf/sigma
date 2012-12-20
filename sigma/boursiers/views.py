# -*- encoding: utf-8 -*-

# from django.contrib.auth.decorators import login_required
# from django.template import loader, RequestContext
# from django.shortcuts import render_to_response
# from django.http import HttpResponseBadRequest
# from sigma.candidatures.models import (
#     Dossier,
#     )


# @login_required
# def nouvelle_allocation(
#     request,
#     template='admin/boursiers/nouvelle_allocation.html',
#     ):
#     d_id = request.GET.get('dossier', None)
#     d_qs = Dossier.objects.filter(id=d_id)
#     error_template = 'admin/error.html'
#     bad_request = False
#     ctx = {}

#     if not d_id or d_qs.count() == 0:
#         bad_request = True
#         ctx['message'] = 'Aucun dossier de correspond à votre requête'

#     if bad_request:
#         rctx = RequestContext(request, ctx)
#         tpl = loader.get_template(error_template)
#         return HttpResponseBadRequest(
#             tpl.render(rctx))
    
#     return render_to_response(
#         template,
#         context_instance=RequestContext(request, ctx),
#         )
