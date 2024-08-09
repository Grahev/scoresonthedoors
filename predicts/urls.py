from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from predicts import views

app_name = 'predicts'

urlpatterns = [
    path('', login_required(views.predicts_home), name='predicts-home'),
    path('<str:date>', login_required(views.predicts_home_date), name='predicts-home-date'),
    path('fixtures/',views.user_predictions, name='user_predictions'),
    path('<int:pk>/', views.match_prediction, name='match_prediction'),
    path('edit/<int:pk>', views.match_prediction_update, name='match_prediction_update'),
    path('<int:pk>/delete',views.delete_view, name='match_prediction_delete'),
    path('<int:pk>/event/delete',views.event_delete, name='match_event_delete'),
    path('<str:user>/',views.user_predictions_list, name='user_prediction_list'),
    path('update/<int:pk>/',views.single_match_update, name='single_match_update'),
    path('points/<int:pk>/',views.match_point_update, name='match_point_update'),
]
