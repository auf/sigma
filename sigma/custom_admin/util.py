# -*- coding: utf-8 -*-


from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.http import HttpResponseForbidden
# from auf.django.permissions import get_rules


class ModelAdmin(admin.ModelAdmin):
    """
    * Ajout d'une stack pour supprimer l'affichage de l'application dans le breadcrumb
    """
    add_form_template = "admin/custom_change_form.html"
    change_form_template = "admin/custom_change_form.html"
    change_list_template = "admin/custom_change_list.html"
    delete_confirmation_template = "admin/custom_delete_confirmation.html"
    delete_selected_confirmation_template = "admin/custom_delete_selected_confirmation.html"
    object_history_template = "admin/custom_object_history.html"



class GuardedAdmin(object):

    pass
    # Seuls les superusers peuvent delete. (Ticket 4862)
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        # TODO: PERMSS
        return super(GuardedAdmin, self) \
            .has_change_permission(request, obj)
        # if obj is not None:
        #     return request.user.has_perm('change', obj)
        # else:
        #     return super(GuardedAdmin, self) \
        #             .has_change_permission(request, obj)

    def get_actions(self, request):
        #Remove delete action from list if not superuser (Ticket 4862)
        actions = super(GuardedAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            actions.pop('delete_selected')
        return actions

    def queryset(self, request):
        # TODO: PERMSS
        return super(GuardedAdmin, self).queryset(request)
        # return get_rules().filter_queryset(
        #     request.user,
        #     'change',
        #     super(GuardedAdmin, self).queryset(request),
        #     )

# Je crois qu'il est preferable de garder l'ordre des deux mixin comme
# tel, pour s'assurer que super(GuardedAdmin, self)... fasse un call a
# ModelAdmin.<methode>
class GuardedModelAdmin(GuardedAdmin, ModelAdmin):
    pass


class GuardedStackedInline(GuardedAdmin, admin.StackedInline):
    pass


class GuardedTabularInline(GuardedAdmin, admin.TabularInline):
    pass

