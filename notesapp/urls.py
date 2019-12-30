from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomepageView.as_view(), name='home'),
    path('notes/new/', views.NoteCreateView.as_view(), name='note_new'),
    path('notes/<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('notes/<int:pk>/edit/', views.NoteEditView.as_view(), name='note_edit'),
]
