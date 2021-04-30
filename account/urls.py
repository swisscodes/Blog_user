from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy, include
from . import views


app_name = 'account'

urlpatterns = [

#path('login1/', views.user_login, name='login1'),
path('login/', auth_views.LoginView.as_view(), name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
# change password urls
path('password_change/',auth_views.PasswordChangeView.as_view(), name='password_change'),
path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
# reset password urls
path('password_reset/', auth_views.PasswordResetView.as_view(success_url= reverse_lazy\
    ('account:password_reset_done')), name='password_reset'),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=\
    reverse_lazy('account:password_reset_complete')), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
# If we didnt set the app_name we could simple use only the below path
# I didnt use only because i was having error of reverse not found
#path('', include('django.contrib.auth.urls')),
path('register/', views.register, name='register'),

]