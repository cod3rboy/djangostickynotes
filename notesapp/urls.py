from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomepageView.as_view(), name='home'),
    path('notes/new/', views.NoteCreateView.as_view(), name='note_new'),
    path('notes/<slug:slug>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('notes/<slug:slug>/edit/', views.NoteEditView.as_view(), name='note_edit'),
    path('notes/<slug:slug>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    path('notes/shared/<slug:slug>/', views.SharedNoteDetailView.as_view(), name='shared_note_detail'),
]
