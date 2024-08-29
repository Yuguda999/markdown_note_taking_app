from django.urls import path
from .views import RegisterView, LoginView, GrammarCheckView, SaveNoteView, ListNotesView, RenderNoteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('grammar-check/', GrammarCheckView.as_view(), name='grammar-check'),
    path('save-note/', SaveNoteView.as_view(), name='save-note'),
    path('notes/', ListNotesView.as_view(), name='list-notes'),
    path('render-note/<int:note_id>/', RenderNoteView.as_view(), name='render-note'),
]