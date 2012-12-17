from admin_tools.dashboard import modules
from django.contrib.admin.models import LogEntry
from django.utils.translation import ugettext_lazy as _

from sigma.candidatures.models import Appel


class AppelsModule(modules.DashboardModule):
    title = 'Appels en cours'
    template = 'appels_module.html'
    simple_css_classes = 'icon_list_module appels_module'

    def init_with_context(self, context):
        if self._initialized:
            return

        for appel in Appel.objects.order_by('-date_fin_appel'):
            self.children.append({
                'nom': appel.nom,
                'statut': 'En cours', # TODO
                'icone': 'appels', # TODO, make class icon_<..> in static/css/dashboard.css
            })

        self._initialized = True


class ActionsRecentesModule(modules.DashboardModule):
    title = 'Actions R&eacute;centes'
    template = 'actions_module.html'
    simple_css_classes = 'actions_module'
    limit = 50
    include_list = None
    exclude_list = None

    def __init__(self, title=None, limit=50, include_list=None,
                 exclude_list=None, **kwargs):
        self.include_list = include_list or []
        self.exclude_list = exclude_list or []
        kwargs.update({'limit': limit})
        super(ActionsRecentesModule, self).__init__(title, **kwargs)

    def init_with_context(self, context):
        if self._initialized:
            return

        qs = LogEntry.objects

        user = context['request'].user
        regions = user.profile.regions.all()
        if user.is_superuser:
            # Les superadmins voient TOUT
            pass
        elif regions:
            qs = qs.filter(user__profile__regions__in=regions)
        else:
            # Celui-ci n'est ni employe ni superadmin
            qs = qs.filter(user__id__exact=user.id)

        if self.include_list:
            qs = qs.filter(_logentry_contenttype_qs(self.include_list))
        if self.exclude_list:
            qs = qs.exclude(_logentry_contenttype_qs(self.exclude_list))

        self.children = qs.select_related('content_type', 'user')[:self.limit]

        if not len(self.children):
            self.pre_content = _('No recent actions.')

        self._initialized = True

    def _logentry_contenttype_qs(contenttypes):
        qset = None
        for contenttype in contenttypes:
            if isinstance(contenttype, ContentType):
                current_qset = Q(content_type__id=contenttype.id)
            else:
                try:
                    app_label, model = contenttype.split('.')
                except:
                    raise ValueError('Invalid contenttype: "%s"' % contenttype)
                current_qset = Q(
                    content_type__app_label=app_label,
                    content_type__model=model
                )
            if qset is None:
                qset = current_qset
            else:
                qset = qset | current_qset
        return qset

