from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SiteUserCreateView.as_view(), name='signup'),
]
