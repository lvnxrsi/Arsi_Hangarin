from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from studentorg.models import Task, Note, SubTask, Category, Priority
from studentorg.forms import TaskForm, NoteForm, SubTaskForm, CategoryForm, PriorityForm

class HomePageView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "home.html"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.count()
        context["completed_tasks"] = Task.objects.filter(status="Completed").count()
        context["in_progress_tasks"] = Task.objects.filter(status="In Progress").count()
        context["pending_tasks"] = Task.objects.filter(status="Pending").count()
        context["total_notes"] = Note.objects.count()
        context["total_categories"] = Category.objects.count()
        context["total_priorities"] = Priority.objects.count()
        context["today"] = timezone.now().date()
        return context

class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "task_list.html"
    paginate_by = 10
    ordering = ["-deadline"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        sort = self.request.GET.get("sort", "-deadline")

        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
                | Q(status__icontains=query)
            )

        valid_fields = ["title", "-title", "deadline", "-deadline", "status", "-status"]
        if sort in valid_fields:
            qs = qs.order_by(sort)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_sort"] = self.request.GET.get("sort", "-deadline")
        context["query"] = self.request.GET.get("q", "")
        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("task-list")

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("task-list")

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_del.html"
    success_url = reverse_lazy("task-list")

class NoteListView(ListView):
    model = Note
    context_object_name = "notes"
    template_name = "note_list.html"
    paginate_by = 10
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        order = self.request.GET.get("order", "-created_at")

        if query:
            qs = qs.filter(
                Q(content__icontains=query)
                | Q(task__title__icontains=query)
            )

        valid_fields = ["created_at", "-created_at", "task__title", "-task__title"]
        if order in valid_fields:
            qs = qs.order_by(order)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_order"] = self.request.GET.get("order", "-created_at")
        context["total_notes"] = Note.objects.count()
        context["today"] = timezone.now().date()
        return context

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy("note-list")

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy("note-list")

class NoteDeleteView(DeleteView):
    model = Note
    template_name = "note_del.html"
    success_url = reverse_lazy("note-list")

class SubTaskListView(ListView):
    model = SubTask
    context_object_name = "subtasks"
    template_name = "subtask_list.html"
    paginate_by = 10
    ordering = ["title"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        order = self.request.GET.get("order", "title")

        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(status__icontains=query)
                | Q(task__title__icontains=query)
            )

        valid_fields = ["title", "-title", "status", "-status", "task__title", "-task__title"]
        if order in valid_fields:
            qs = qs.order_by(order)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_order"] = self.request.GET.get("order", "title")
        return context

class SubTaskCreateView(CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"
    success_url = reverse_lazy("subtask-list")

class SubTaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtask_form.html"
    success_url = reverse_lazy("subtask-list")

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = "subtask_del.html"
    success_url = reverse_lazy("subtask-list")

class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "category_list.html"
    paginate_by = 10
    ordering = ["name"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        order = self.request.GET.get("order", "name")

        if query:
            qs = qs.filter(Q(name__icontains=query))

        valid_fields = ["name", "-name"]
        if order in valid_fields:
            qs = qs.order_by(order)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_order"] = self.request.GET.get("order", "name")
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("category-list")

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("category-list")

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "category_del.html"
    success_url = reverse_lazy("category-list")

class PriorityListView(ListView):
    model = Priority
    context_object_name = "priorities"
    template_name = "priority_list.html"
    paginate_by = 10
    ordering = ["name"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        order = self.request.GET.get("order", "name")

        if query:
            qs = qs.filter(Q(name__icontains=query))

        valid_fields = ["name", "-name", "created_at", "-created_at", "updated_at", "-updated_at"]
        if order in valid_fields:
            qs = qs.order_by(order)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_order"] = self.request.GET.get("order", "name")
        context["total_priorities"] = Priority.objects.count()
        return context

class PriorityCreateView(CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = "priority_form.html"
    success_url = reverse_lazy("priority-list")

class PriorityUpdateView(UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = "priority_form.html"
    success_url = reverse_lazy("priority-list")

class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = "priority_del.html"
    success_url = reverse_lazy("priority-list")
