from re import L
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from leagues.models import League, WeeklyPoint, MonthlyPoint
from predicts.models import MatchPrediction
from leagues.forms import LeagueCreateModelForm, LeagueJoinPinForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core import serializers
from django.db.models import Count, Sum, Avg, Case, When, IntegerField, F, Value
from django.db.models.functions import Round
from django.db.models.aggregates import Count
import json

from django.urls import reverse_lazy

# Create your views here.

def leagues_home(request):
    context = {}
    return render(request, 'leagues_home.html', context)

def maximum_leagues(request):
    return render(request,'maximum_leagues.html')


class LeaguesListView(ListView):
    model = League
    template_name = 'leagues_home.html'
    context_object_name = 'leagues'

    def get_queryset(self):
        return League.objects.filter(users__username = self.request.user)


class LeagueCreateView(CreateView):
    form_class = LeagueCreateModelForm
    template_name = 'league_create.html'
    success_url = reverse_lazy('leagues:leagues-home')
    


    def form_valid(self, form):
        u = self.request.user
        users_admins = League.objects.filter(admin = u)
        print(f'len of users admins leagues: {len(users_admins)}')
        if len(users_admins) <= 3:
            form.instance.admin = u
            self.object = form.save(commit=False)
            self.object.save()
            l = League.objects.get(name=form.instance.name)
            l.users.add(u)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return redirect('leagues:maximum-leagues')

class LeagueDetailView(DetailView):

    model = League
    template_name = 'league_detail.html'
    

    def get_conext_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = request.user.username
        context['p'] = MatchPrediction.objects.filter(user=user)
        return context
        

def league_view(request):
    """view for list of users leagues"""
    user = request.user.username
    leagues = League.objects.filter(users=User.objects.get(username=user))
    context = {
        'leagues':leagues,
    }
    return render(request, 'predictor/league.html', context)



def league_details(request,pk):
    league = League.objects.get(id=pk)
    # Retrieve weekly points for each user in the league
    weekly_points = WeeklyPoint.objects.filter(user__leagues=league)

    # Retrieve monthly points for each user in the league
    monthly_points = MonthlyPoint.objects.filter(user__leagues=league)
    
    
    
    
    context = {
        'league': league 
    }

    return render(request,'league_detail.html', context)

def leave_league(request,pk):
    league = League.objects.get(id=pk)
    user = request.user
    context = {
        'league': league
    }

    return render(request,'leave_league.html', context)

def leave_league_confirm(request,pk):
    league = League.objects.get(id=pk)
    user = request.user

    if league.name == 'MASTER LEAGUE':
        messages.error(request, 'You cant leave MASTER LEAGUE')
        return redirect('/leagues')
    else:
        league.users.remove(user)
        messages.info(request,f'You leave {league.name}.')
        return redirect('leagues:leagues-home')

def join_league(request):
    print(request.POST)
    leagues = League.objects.all()

    if request.method == 'POST':
        form = request.POST
        try:
            league = League.objects.get(name=form['name'])
            print(league.admin)
        except:
            league = ''

    context = {
        'leagues':leagues
    }
    return render(request,'join_league.html', context)


def join_league_pin(request, pk):
    league = League.objects.get(id=pk)
    form = LeagueJoinPinForm()
    user = request.user
    print(league)

    if request.method == 'POST':
        form = LeagueJoinPinForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data['pin']
            print(f'pin: {type(pin)}')
            print(f'league pin:{league.pin}')
            if pin == league.pin:
                print('match')
                league.users.add(user)
                messages.info(request,f'You join {league.name}.')
                return redirect('/leagues')
            else:
                #//TODO add message about wrong pin.
                print('pin not match')

    context = {
        'league':league,
        'form': form
    }
    return render(request,'join_league_confirm.html',context)


def league_delete(request, pk):
    league = get_object_or_404(League, id=pk)
    user = request.user
    context = {}

    if request.method == 'POST':
        if user.id == league.admin.id:
            league.delete()
            return redirect('leagues:leagues-home')
        else:
            messages.info(request,f'You must be administrator to delete {league.name}.')
            return redirect('leagues:leagues-home')

    return render(request, 'delete_league.html', context)

def league_old_points(request):
    queryset = (
        MatchPrediction.objects.values(
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
            .order_by('-total_points')
            
    )
    context = {'queryset': queryset}
   
    return render(request, 'league_old_points.html', context=context)

def user_statistics(request,pk):
        # Ensure the requested user exists, or return a 404 page
    user = get_object_or_404(User, pk=pk)

    # Filter predictions for the specified user
    user_predictions = MatchPrediction.objects.filter(user=user)

    common_home_teams = user_predictions.values('homeTeamName').annotate(total=Count('homeTeamName')).order_by('-total')[:5]
    common_away_teams = user_predictions.values('awayTeamName').annotate(total=Count('awayTeamName')).order_by('-total')[:5]
    common_goal_scorers = user_predictions.values('goalScorerName').annotate(total=Count('goalScorerName')).order_by('-total')[:5]

    queryset = (
        MatchPrediction.objects.values(
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
            .filter(user_id=pk).order_by('-total_points')
    )
  
    context = {
        'target_user': user,
        'common_home_teams': common_home_teams,
        'common_away_teams': common_away_teams,
        'common_goal_scorers': common_goal_scorers,
        'queryset': queryset,
    }

    return render(request, 'user_statistics.html', context)