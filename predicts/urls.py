from django.contrib import admin
from django.urls import path
from predicts.views import predicts_list, match_prediction, predicts_home,user_predictions

app_name = 'predicts'
urlpatterns = [
    path('', predicts_home, name='predicts-home'),
    path('fixtures/<int:league>/<int:year>', predicts_list, name='predicts-list'),
    path('fixtures/<int:league>/<int:year>/<int:match_id>', match_prediction, name='predicts-create'),
    path('fixtures/<int:pk>',user_predictions, name='user_predictions'),
]
