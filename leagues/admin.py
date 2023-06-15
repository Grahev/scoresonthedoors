from django.contrib import admin
from leagues.models import League, WeeklyPoint, MonthlyPoint


admin.site.register(League),
admin.site.register(WeeklyPoint),
admin.site.register(MonthlyPoint),