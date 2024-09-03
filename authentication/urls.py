# authentication/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)