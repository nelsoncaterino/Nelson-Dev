from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count
from app.models import IPVisit

class IPVisitAdmin(admin.ModelAdmin):
    change_list_template = "admin/ipvisit_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('stats/', self.admin_site.admin_view(self.stats_view), name='ipvisit_stats'),
        ]
        return custom_urls + urls

    def stats_view(self, request):
        # Exemple : regrouper par pays
        visits_by_country = (
            IPVisit.objects.values('country')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        countries = [entry['country'] or 'Unknown' for entry in visits_by_country]
        counts = [entry['count'] for entry in visits_by_country]

        context = dict(
            self.admin_site.each_context(request),
            countries=countries,
            counts=counts,
        )
        return TemplateResponse(request, "admin/ipvisit_stats.html", context)

admin.site.register(IPVisit, IPVisitAdmin)
