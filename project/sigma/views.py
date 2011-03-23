# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, redirect
from forms import DisciplineForm

@login_required
def mes_disciplines(request, ):
    if request.method == "POST":
        form = DisciplineForm(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="Les disciplines ont été enregistrées.")
            return redirect(reverse('admin:index'))
    else:
        form = DisciplineForm(instance=request.user.profile)
    
    c = {'form' : form, }
    return render_to_response("admin/sigma/mes_disciplines.html", \
                               Context(c), \
                               context_instance = RequestContext(request))
