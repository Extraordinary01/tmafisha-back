from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('password-reset/', UserPasswordReset.as_view(), name='password-reset'),
    path('password-reset/password-reset-done/', UserPasswordResetDone.as_view(), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', UserPasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('password-reset/<uidb64>/set-password/password-reset-complete/', UserPasswordResetComplete.as_view(), name='password-reset-complete'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout')
]