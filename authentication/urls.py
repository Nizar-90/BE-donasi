# authentication/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, LoginView, LogoutView, UserProfileUpdateView, UserDetailView, DonationCreateView, DonationListView, InputDonasiAPIView, DonationHistoryListAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    
    path('donations/create/', DonationCreateView.as_view(), name='create-donation'),
    path('donations/', DonationListView.as_view(), name='donation-list'),
    path('donations/input/', InputDonasiAPIView.as_view(), name='input_donasi'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('donations/history/', DonationHistoryListAPIView.as_view(), name='donation_history'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  