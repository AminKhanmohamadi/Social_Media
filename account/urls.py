from django.urls import path
from .views import *
app_name = 'account'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/' , UserProfileView.as_view(), name='profile'),
    path('reset/' , UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done/' , UserPasswordResetDoneView.as_view(), name='reset_password_done'),
    path('confirm/<uidb64>/<token>/' , PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/' , PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id>/' , UserFollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/' , UserUnfollowView.as_view(), name='unfollow'),
    path('edit_user/' , EditUserView.as_view(), name='edit_user'),
]