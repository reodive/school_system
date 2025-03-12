from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_note, name='create_note'),
    path('<int:note_id>/', views.note_detail, name='note_detail'),
    # edit_note ビューも追加する場合
    # path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
]
