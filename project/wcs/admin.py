# -*- encoding: utf-8 -*-

from django.contrib import admin
from models import WCSAppel, WCSChamps
from forms import WCSChampsForm
from wrappers import WCSAppel as WCSAppelWrapper

class WCSMappingAdminInline(admin.TabularInline):
    model = WCSChamps
    form = WCSChampsForm

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(WCSMappingAdminInline, self).get_formset(request, obj, **kwargs)
        if obj is not None:
            wcs_wrapper = WCSAppelWrapper()
            statut, data = wcs_wrapper.test(obj.wcs)
            formset.form.declared_fields['wcs'].choices =  [('', '---------')] + [(c,c) for c in data]
        return formset

class WCSAppelAdmin(admin.ModelAdmin):
    inlines = (WCSMappingAdminInline, )
    
    


admin.site.register(WCSAppel, WCSAppelAdmin)
