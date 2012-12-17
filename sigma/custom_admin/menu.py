# -*- encoding: utf-8 -*-

"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'SIGMA.menu.CustomMenu'
"""

from admin_tools.menu import Menu
from admin_tools.menu.items import MenuItem, Bookmarks
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class MainMenu(Menu):
    """
    Custom Menu for SIGMA admin site.
    """
    def __init__(self, *args, **kwargs):
        super(MainMenu, self).__init__(*args, **kwargs)
        self.children += [
            MenuItem('Accueil', reverse('admin:index')),
            MenuItem('Appels', reverse('admin:candidatures_appel_changelist')),
            MenuItem('Candidats', reverse('admin:candidatures_dossier_changelist')),
            MenuItem('Allocataires', reverse('admin:boursiers_boursier_changelist')),
            MenuItem('Experts', reverse('admin:candidatures_expert_changelist')),
        ]

    def init_with_context(self, context):
        super(MainMenu, self).init_with_context(context)
        if context['request'].user.is_superuser:
            # Added here because these superuser options are no longer
            # available on the dashboard
            self.children += [
                MenuItem('-- Configuration', reverse('admin:app_list', kwargs={'app_label': 'candidatures'})),
                MenuItem('-- Utilisateurs', reverse('admin:app_list', kwargs={'app_label': 'auth'})),
            ]
