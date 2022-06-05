from django.shortcuts import render

# Create your views here.

def leagues_home(request):
    context = {}
    return render(request, 'leagues_home.html', context)