from re import L
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from leagues.models import League
from predicts.models import MatchPrediction
from leagues.forms import LeagueCreateModelForm, LeagueJoinPinForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy

# Create your views here.

def leagues_home(request):
    context = {}
    return render(request, 'leagues_home.html', context)


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
        if len(users_admins) <= 3:
            self.object = form.save(commit=False)
            self.object.save()
            l = League.objects.get(name=form.instance.name)
            l.users.add(u)
            return HttpResponseRedirect(self.get_success_url())
        else:
            form.add_error('name', 'You reach maximum number of leagues. Delete old leagues before create new.')

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
    table = []
    create_date = league.create_date

    #create dict with user points
    for user in league.users.iterator():  
        points_dict = {}
        user_points = 0
        #print(user)
        predictions = MatchPrediction.objects.filter(user=user).filter(match__date__gte = create_date)
        print(predictions)
        for match in predictions.iterator():
            if match.points:
                print(match.points)
                user_points += match.points
        print(f'{user} points:{user_points}')
        points_dict = {
            'name': user.username,
            'points' : user_points
            }

        table.append(points_dict)
    
    #sort table by points
    points_table= sorted(table, key=lambda d: d['points'], reverse=True)
    
    context = {
        'league': league,
        'table' : points_table,
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