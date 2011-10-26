# -*- encoding: utf-8 -*-

"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'SIGMA.menu.CustomMenu'
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu
from admin_tools.menu.items import MenuItem


class MonCompteMenuItem(MenuItem):
    """
    Menu personnel destiné à recevoir les fonctionnalités spéciales de 
    l'utilisateur connecté.
    """
    title = "Mon compte"
    url = reverse('admin:index')

    mes_disciplines = items.MenuItem(_('Mes disciplines'), reverse('mes_disciplines'))
   
    def init_with_context(self, context):
        request = context['request']

        self.title = request.user

        if 'experts' in [g.name.lower() for g in request.user.groups.all()]:
            self.children.append(self.mes_disciplines)

class CustomMenu(Menu):
    """
    Custom Menu for SIGMA admin site.
    """

    mon_compte = items.MenuItem(_('Mon compte'), reverse('admin:index'))

    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            # Désactiver Mes Disciplines pour les experts
            #MonCompteMenuItem(),
            items.Bookmarks(),
            items.MenuItem('Sigma', children=[
                items.MenuItem('Appels', reverse('admin:sigma_appel_changelist')),
                items.MenuItem('Dossiers', reverse('admin:sigma_dossier_changelist')),
                items.MenuItem('Boursiers', reverse('admin:suivi_boursier_changelist')),
                items.MenuItem('Experts', reverse('admin:sigma_expert_changelist'))
            ])
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        request = context['request']
        return super(CustomMenu, self).init_with_context(context)
