from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from . import views


app_name = 'account'

urlpatterns = [
    # Likes
    path('star/', views.star, name='star'),
    # Reviews
    path('rate_us/', views.ReviewCreateView.as_view(), name='review'),
    path('review/results/', views.ReviewListView.as_view(), name='review_results'),
    path('review/update/<int:pk>/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('delete/<int:pk>/', views.review_delete, name='review_delete'),
    # Register / Login-Logout
    path('register/', views.UserCreateView.as_view() ,name='register'),
    path('activate/<slug:uidb64>/<slug:token>', views.account_activation ,name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html', redirect_authenticated_user=True) ,name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    # User Profile-user / Update / Delete
    path('profile/<slug:slug>/', views.ProfileDetailView.as_view(), name='profile'),
    path('<slug:slug>/profile_information/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('<slug:slug>/personal_information/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('<slug:slug>/user/confirm_delete/', views.UserDeleteView.as_view(), name='user_delete'),
    # Password Change
    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    # Password Reset
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/passwordreset/password_reset_confirm.html',success_url = reverse_lazy('account:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset_complete/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]
