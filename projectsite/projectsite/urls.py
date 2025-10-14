from django.contrib import admin
from django.urls import path
from studentorg.views import (
    HomePageView,
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    NoteListView, NoteCreateView, NoteUpdateView, NoteDeleteView,
    SubTaskListView, SubTaskCreateView, SubTaskUpdateView, SubTaskDeleteView
)
from studentorg import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.HomePageView.as_view(), name="home"),

    # Task URLs
    path("task_list/", TaskListView.as_view(), name="task-list"),
    path("task_list/add/", TaskCreateView.as_view(), name="task-add"),
    path("task_list/<pk>/", TaskUpdateView.as_view(), name="task-update"),
    path("task_list/<pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    # Note URLs
    path("note_list/", NoteListView.as_view(), name="note-list"),
    path("note_list/add/", NoteCreateView.as_view(), name="note-create"),
    path("note_list/<pk>/", NoteUpdateView.as_view(), name="note-update"),
    path("note_list/<pk>/delete/", NoteDeleteView.as_view(), name="note-delete"),

    path("subtask_list/", SubTaskListView.as_view(), name="subtask-list"),
    path("subtask_list/add/", SubTaskCreateView.as_view(), name="subtask-create"),
    path("subtask_list/<pk>/", SubTaskUpdateView.as_view(), name="subtask-update"),
    path("subtask_list/<pk>/delete/", SubTaskDeleteView.as_view(), name="subtask-delete"),
]
