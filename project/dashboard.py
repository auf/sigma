# -*- encoding: utf-8 -*

"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'SIGMA.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'SIGMA.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for SIGMA.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.ModelList('SIGMA', [
            'sigma.models.Appel',
            'sigma.models.Dossier',
            'suivi.models.Boursier'
        ]))
        self.children.append(modules.ModelList('Configuration', [
            'sigma.models.NiveauEtude',
            'sigma.models.Public',
            'sigma.models.TypeConformite',
            'sigma.models.TypePiece'
        ]))
        self.children.append(modules.ModelList('Utilisateurs', [
            'django.contrib.auth.models.User',
            'django.contrib.auth.models.Group',
            'sigma.models.GroupeRegional',
            'sigma.models.Expert'
        ]))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))
