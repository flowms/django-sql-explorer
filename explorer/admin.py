from django.contrib import admin

from explorer.actions import generate_report_action
from explorer.models import Query
from explorer.forms import QueryForm
from explorer.app_settings import (
    EXPLORER_DEFAULT_CONNECTION, EXPLORER_CONNECTIONS, ENABLE_TASKS
)


class QueryAdmin(admin.ModelAdmin):
    form = QueryForm
    list_display = ('title', 'description', 'run_count', 'avg_duration', 'last_run_date', 'created_by_user',)
    list_filter = ('title',)
    raw_id_fields = ('created_by_user',)
    fields = ['title', 'description', 'sql',]
    #view_on_site = False

    fields.append('snapshot') if ENABLE_TASKS else None
    fields.append('connection') if len(EXPLORER_CONNECTIONS) > 1 else None

    actions = [generate_report_action()]

    def run_count(self, obj):
        return obj.get_run_count()

    def avg_duration(self, obj):
        return str(int(obj.avg_duration())) + ' ms'



admin.site.register(Query, QueryAdmin)
