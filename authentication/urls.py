from django.contrib import admin
from django.urls import path, include, reverse_lazy
from authentication.views import home, signup, user_logout, activate, Login, signup_confirmation, matchday_cache_clearout, panel
from django.contrib.auth import views as auth_views



app_name = 'authentication'
urlpatterns = [
    path('', home,name='home'),
    path('login/', Login.as_view(),name='login'),
    path('signup/', signup,name='signup'),
    path('logout/', user_logout,name='logout'),
    path('signup/confirm/', signup_confirmation,name='signup_confirmation'),
    path('activate/<uidb64>/<token>', activate.as_view(), name='activate'),
    path('clear_cache/', matchday_cache_clearout, name='matchday_cache_clearout'),
    path('panel/', panel, name='panel'),

    
    #password recovery
    
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name ='password_reset.html',
        email_template_name = 'password_reset_email.html',
        success_url='../reset_password_sent',
    ), name='reset_password'),
    
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done' ),
    
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        success_url = reverse_lazy("authentication:password_reset_complete")
    ), name='password_reset_confirm'),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'password_reset_complete.html'
    ),name='password_reset_complete'),
]