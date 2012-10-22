# -*- coding: utf-8 -*-


from django.contrib import admin

from auf.django.permissions import get_rules


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



class GuardedModelAdmin(ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return request.user.has_perm('change', obj)
        else:
            return super(GuardedModelAdmin, self) \
                    .has_change_permission(request, obj)

    def queryset(self, request):
        return get_rules().filter_queryset(
            request.user,
            'change',
            super(GuardedModelAdmin, self).queryset(request)
        )
