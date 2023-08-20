from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET, SET_NULL, DO_NOTHING
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
from predicts.models import MatchPrediction, Week
import datetime
from django.db.models import Q, Sum
from operator import itemgetter
from django.utils import timezone



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
        current_week = Week.objects.get(pk=1)
        print(f'current_week: {current_week}')
        #return weekly points for each user in league for each week from create date to current week
        users = self.users.all()
        weekly_points = {}
        l = League.objects.get(id=self.id)
        for user in users:
            # weekly_points[user] = {}
            # for week in range(1, 52):
            points = MatchPrediction.objects.filter(
                user = user, 
                match_date__week = current_week.week_number, 
                match_date__year = current_week.year
                ).aggregate(models.Sum('points'))['points__sum']
            if points == None:
                pass
            else:
                #update or create weekly points
                weekly_points, created = WeeklyPoint.objects.get_or_create(
                    user = user, 
                    
                    week_number = current_week.week_number, 
                    year = current_week.year,
                    league = l
                    )
                weekly_points.points = points
                weekly_points.save()
                
        
        return weekly_points
    
    def monthly_points_calc(self):
        """Calculate monthly points for each user in league - takes last for weeks to calcuate sum of points for each user then create MonthlyPoint object for each user in league.
        Month is based on current month"""
        points_dict = {
            1: 25,
            2: 18,
            3: 15,
            4: 12,
            5: 10,
            6: 8,
            7: 6,
            8: 4,
            9: 2,
            10: 1
        }
        #create monthly points for each user in league or placec from 1 to 10
        users = self.users.all()
        #get current week number
        current_week = Week.objects.get(pk=1)
        #get current month
        current_month = datetime.date.today().month
        
        end_month_table =  {}
        for user in users:
            #get user weekly points from last 4 weeks
            weekly_points = WeeklyPoint.objects.filter(user = user, week_number__gte = current_week.week_number - 4, year = self.current_year())
            #get weekly points sume
            weekly_points_sum = weekly_points.aggregate(Sum('points'))['points__sum']
            #append to dict
            end_month_table[user] = weekly_points_sum

        #sort dict by points
        sorted_weekly_points = sorted(end_month_table.items(), key=itemgetter(1), reverse=True)
            
        #get top 10 users
        top_ten = sorted_weekly_points[:10]
        #create monthly points for each user
        for i, user in enumerate(top_ten):
            place = int(i+1)
            monthly_points, created = MonthlyPoint.objects.get_or_create(
                user = user[0], 
                #TODO: change the way how to calculate month - use month 1 when season start and keep counting???
                month=current_month, 
                year = self.current_year(),
                league = League.objects.get(id = self.id)
                )
            monthly_points.points = points_dict[i+1]
            monthly_points.place = place 
            monthly_points.save()
            print(f'{user[0]} - place: {i+1} - points: {points_dict[i+1]}')

    
    def table(self):
        #return table of users and their points
        # Get the current month and year
        current_month = timezone.now().month
        current_year = timezone.now().year
        table = []
        users = self.users.all()
        for user in users:
            weekly_points = WeeklyPoint.objects.filter(user = user).filter(league = self.id)
            four_weekly_points = weekly_points.order_by('-week_number')[:4]
            monthly_points = MonthlyPoint.objects.filter(
                Q(user = user) & Q(created_at__gte=self.create_date))
            # Calculate the sum of monthly points
            monthly_points_sum = monthly_points.aggregate(Sum('points'))['points__sum']
             # Provide a default value of 0 for monthly_points_sum if it is None
            monthly_points_sum = monthly_points_sum or 0
            
            #weekly points sum calculation
            weekly_sum = WeeklyPoint.objects.filter(
                user=user,
                league = self.id,
                created_at__month=current_month,
                created_at__year=current_year
                ).aggregate(total_points=models.Sum('points'))['total_points']
            
            # If there are no points for the current month, default to 0
            weekly_sum = weekly_sum or 0
            
            table.append({
                'username': user.username,
                'weekly_points': weekly_points,
                'four_weekly_points': four_weekly_points,
                'monthly_points': monthly_points,
                'monthly_points_sum': monthly_points_sum,  # Add the sum to the table
                'weekly_sum': weekly_sum
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
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='weekly_points')

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
    place = models.PositiveIntegerField(default=0)

    # class Meta:
    #     unique_together = ('user', 'month', 'year')

    def update_points(self, points):
        self.points += points
        self.save()

    def __str__(self):
        return f'{self.user} - {self.month} - {self.year} - {self.points} - {self.place}'