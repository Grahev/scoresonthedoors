from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET, SET_NULL, DO_NOTHING
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
from predicts.models import MatchPrediction
import datetime
from django.db.models import Q, Sum
from operator import itemgetter



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
   
    
    def weekly_points_calc(self):
        current_week = datetime.date.today().isocalendar()[1]
        print(f'current_week: {current_week}')
        #return weekly points for each user in league for each week from create date to current week
        users = self.users.all()
        weekly_points = {}
        for user in users:
            # weekly_points[user] = {}
            for week in range(1, 52):
                points = MatchPrediction.objects.filter(user = user, match_date__week = week, match_date__year = self.current_year()).aggregate(models.Sum('points'))['points__sum']
                if points == None:
                    pass
                else:
                    # weekly_points[user][week] = points
                    #update or create weekly points
                    weekly_points, created = WeeklyPoint.objects.get_or_create(user = user, week_number = week, year = self.current_year())
                    weekly_points.points = points
                    weekly_points.save()
                
        
        return weekly_points
    
    def table(self):
        #return table of users and their points
        table = []
        users = self.users.all()
        for user in users:
            weekly_points = WeeklyPoint.objects.filter(user = user)
            four_weekly_points = weekly_points.order_by('-week_number')[:4]
            monthly_points = MonthlyPoint.objects.filter(
                Q(user = user) & Q(created_at__gte=self.create_date))
            # Calculate the sum of monthly points
            monthly_points_sum = monthly_points.aggregate(Sum('points'))['points__sum']
             # Provide a default value of 0 for monthly_points_sum if it is None
            monthly_points_sum = monthly_points_sum or 0
            table.append({
                'username': user.username,
                'weekly_points': weekly_points,
                'four_weekly_points': four_weekly_points,
                'monthly_points': monthly_points,
                'monthly_points_sum': monthly_points_sum  # Add the sum to the table
            })

         # Sort the table based on monthly_points_sum in descending order
        sorted_table = sorted(table, key=itemgetter('monthly_points_sum'), reverse=True)
        
        return sorted_table
    
class WeeklyPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_points')
    week_number = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
        # unique_together = ('user', 'week_number', 'year')

    def update_points(self, points):
        self.points += points
        self.save()

    def __str__(self):
        return f'{self.user} - {self.week_number} - {self.year} - {self.points}'


class MonthlyPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monthly_points')
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    points = models.IntegerField(default=0)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='monthly_points')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'month', 'year')

    def update_points(self, points):
        self.points += points
        self.save()