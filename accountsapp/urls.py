from django.urls import path
from . import views


urlpatterns = [
    path('accounts/signup/', views.SiteUserCreateView.as_view(), name='signup'),
    path('profile/', views.SiteUserProfileView.as_view(), name='profile'),
    path('profile/change/', views.SiteUserProfileChangeView.as_view(), name='profile_change'),
]
