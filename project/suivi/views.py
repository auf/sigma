# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, redirect
from sigma.models import Dossier

