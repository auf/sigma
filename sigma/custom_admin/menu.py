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


class CustomMenu(Menu):
    """
    Custom Menu for SIGMA admin site.
    """
    mon_compte = MenuItem(_('Mon compte'), reverse('admin:index'))

    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            MenuItem(_('Dashboard'), reverse('admin:index')),
            Bookmarks(),
            MenuItem('Sigma', children=[
                MenuItem(
                    'Appels', reverse('admin:candidatures_appel_changelist')
                ),
                MenuItem(
                    'Dossiers de candidature',
                    reverse('admin:candidatures_dossier_changelist')
                ),
                MenuItem(
                    'Boursiers', reverse('admin:boursiers_boursier_changelist')
                ),
                MenuItem(
                    'Experts', reverse('admin:candidatures_expert_changelist')
                ),
                MenuItem('Formulaire WCS', reverse('wcs-formulaire_wcs')),
            ])
        ]
