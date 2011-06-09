# -*- encoding: utf-8 -*-

import csv
from django.contrib import admin
from django.utils.functional import update_wrapper
from django.http import Http404, HttpResponse, HttpResponseBadRequest

SEPARATOR = u"__"

class ExportAdmin(admin.ModelAdmin):
    change_list_template = 'export/change_list.html'

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^export/$',
                wrap(self.export),
                name='%s_%s_export' % info),
        )
        urlpatterns += super(ExportAdmin, self).get_urls()
        return urlpatterns

    def get_object_value(self, obj, header):
        segments = header.split(SEPARATOR)
        segments.reverse()
        prop = segments.pop()
        if len(segments) == 0:
            return getattr(obj, prop, "")
        else:
            try:
                child = getattr(obj, prop, None)
                return self.get_object_value(child, ".".join(segments))
            except:
                return ""

    def export(self, request):

        csv_fields = getattr(self, 'csv_fields', None)

        if csv_fields is None:
            fields_name = [f.name for f in  self.model._meta.fields]
            for fk in self.model._meta._related_objects_cache.keys():
                fields_name = fields_name + [u"%s%s%s" % (fk.var_name, SEPARATOR, f.name) for f in fk.model._meta.fields]
            csv_fields = fields_name
        qs = self.queryset(request)

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(self.model._meta.verbose_name_plural)

        writer = csv.writer(response)

        headers = []
        for attr in csv_fields:
            headers.append(attr)
        writer.writerow(headers)

        for o in qs:
            row = []
            for attr in csv_fields:
                value = self.get_object_value(o, attr)
                row.append(value)
            writer.writerow(row)

        return response
