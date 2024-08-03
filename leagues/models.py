from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET, SET_NULL, DO_NOTHING
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
from predicts.models import MatchPrediction
import datetime
from django.db.models import Q, Count, Sum, Avg, Case, When, IntegerField, F, Value
from django.db.models.functions import Round
from django.db.models.aggregates import Count
from operator import itemgetter
from django.utils import timezone

import logging

from django.conf import settings

logging.basicConfig(
    level=logging.DEBUG,
    filename='montly points log.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' 
)

logger = logging.getLogger('points')




# Create your models here.
class League(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    pin = models.IntegerField()
    admin = models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name='league_admin')
    users = models.ManyToManyField(User, related_name='leagues')
    create_date = models.DateTimeField(auto_now_add=True)
    rules = models.TextField(max_length=500, blank=True)

    

    def __str__(self):
        return self.name
    
    def start_week(self):
        #return week number when league was created
        return self.create_date.isocalendar()[1]
    
    def current_year(self):
        #return current year
        return datetime.date.today().year
    
    def old_points(self):
        queryset = (
            MatchPrediction.objects.filter(user__in=self.users.all(), match__date__gt = settings.FILTER_DATE)  # Filter predictions for users in this league
            .values(
                'user_id',
                'user__username'
            )
            .annotate(
                total_predictions_by_user=Count('id'),
                total_points=Sum('points'),
                avg_points_per_user=Round(Avg(F('points') * 1.0), 2),
                points_6=Count(Case(When(points=6, then=Value(1)), output_field=IntegerField())),
                points_4=Count(Case(When(points=4, then=Value(1)), output_field=IntegerField())),
                points_3=Count(Case(When(points=3, then=Value(1)), output_field=IntegerField())),
                points_2=Count(Case(When(points=2, then=Value(1)), output_field=IntegerField())),
                points_1=Count(Case(When(points=1, then=Value(1)), output_field=IntegerField())),
                points_0=Count(Case(When(points=0, then=Value(1)), output_field=IntegerField()))
            )
            .order_by('-total_points'))
        return queryset
