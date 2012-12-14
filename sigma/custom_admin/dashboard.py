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

from admin_tools.dashboard import modules, Dashboard
from django.utils.translation import ugettext_lazy as _


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for SIGMA.
    """
    def init_with_context(self, context):
        self.children.append(modules.ModelList('SIGMA', [
            'sigma.candidatures.models.Appel',
            'sigma.candidatures.models.Dossier',
            'sigma.boursiers.models.Boursier',
            'sigma.candidatures.models.Expert'
        ]))
        self.children.append(modules.ModelList('Configuration', [
            'sigma.candidatures.models.Public',
            'sigma.candidatures.models.TypeConformite',
            'sigma.candidatures.models.TypePiece'
        ]))
        self.children.append(modules.ModelList('Utilisateurs', [
            'django.contrib.auth.models.User',
            'django.contrib.auth.models.Group',
            'sigma.candidatures.models.GroupeRegional',
        ]))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))
