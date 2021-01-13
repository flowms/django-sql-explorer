from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group

from explorer.actions import generate_report_action
from explorer.models import Query
from explorer.forms import QueryForm
from explorer.app_settings import (
    EXPLORER_DEFAULT_CONNECTION, EXPLORER_CONNECTIONS, ENABLE_TASKS
)


class QueryAdmin(admin.ModelAdmin):
    form = QueryForm
    raw_id_fields = ('created_by_user',)
    fields = ['title', 'description', 'sql', 'group_id']
    #view_on_site = False

    fields.append('snapshot') if ENABLE_TASKS else None
    fields.append('connection') if len(EXPLORER_CONNECTIONS) > 1 else None

    actions = [generate_report_action()]

    def run_count(self, obj):
        return obj.get_run_count()

    def avg_duration(self, obj):
        return str(int(obj.avg_duration())) + ' ms'

    def can_change(self, obj):
        return self.request.user.has_perm('explorer.change_query')

    def title_url(self, obj):
        if self.can_change(self):
            return format_html("<b><a href='./{qry}'>{title}</a></b>", qry=obj.pk, title=obj.title)
        else:
            return format_html("<b><a href='/explorer/{qry}/?fullscreen=1&rows=1000'>{title}</a></b>", qry=obj.pk, title=obj.title)
    title_url.short_description = "Report Name"
    title_url.admin_order_field = 'title'

    def get_queryset(self, request):
        qs = super(QueryAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            groups = Group.objects.filter(user = request.user)
            qs = qs.filter(group_id__in=groups)
        self.request = request
        return qs

    def get_list_display(self, request, obj=None):
        if request.user.has_perm('explorer.change_query'):
            list_display = ['title_url', 'description', 'group_id', 'run_count', 'avg_duration', 'last_run_date', 'created_by_user']
        else:
            list_display = ['title_url', 'description',]
        return list_display

    def get_list_filter(self, request, obj=None):
        if request.user.has_perm('explorer.change_query'):
            list_filter = ('title', 'group_id')
        else:
            list_filter = ('title',)
        return list_filter






admin.site.register(Query, QueryAdmin)
