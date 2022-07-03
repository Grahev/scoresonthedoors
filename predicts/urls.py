from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from predicts.views import  match_prediction, predicts_home,user_predictions, match_prediction,match_prediction_update,delete_view, user_predictions_list

app_name = 'predicts'
urlpatterns = [
    path('', login_required(predicts_home), name='predicts-home'),
    path('fixtures/',user_predictions, name='user_predictions'),
    path('<int:pk>/', match_prediction, name='match_prediction'),
    path('edit/<int:pk>', match_prediction_update, name='match_prediction_update'),
    path('<int:pk>/delete',delete_view, name='match_prediction_delete'),
    path('<str:user>/',user_predictions_list, name='user_prediction_list'),
]
