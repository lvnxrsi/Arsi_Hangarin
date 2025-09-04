from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from studentorg.models import Task, SubTask, Note, Category, Priority


class Command(BaseCommand):
    help = 'Create initial data for Tasks, SubTasks, and Notes'

    def handle(self, *args, **kwargs):
        self.create_tasks(10)
        self.create_subtasks(20)
        self.create_notes(15)

    def create_tasks(self, count):
        fake = Faker()
        statuses = ["Pending", "In Progress", "Completed"]

        for _ in range(count):
            Task.objects.create(
                title=fake.sentence(nb_words=5),                  # Task title
                description=fake.paragraph(nb_sentences=3),       # Task description
                status=fake.random_element(elements=statuses),    # Task status
                deadline=timezone.make_aware(fake.date_time_this_month()),  # Deadline
                category=Category.objects.order_by("?").first(),
                priority=Priority.objects.order_by("?").first(),
            )

        self.stdout.write(self.style.SUCCESS(' Tasks created.'))

    def create_subtasks(self, count):
        fake = Faker()
        statuses = ["Pending", "In Progress", "Completed"]

        for _ in range(count):
            SubTask.objects.create(
                task=Task.objects.order_by("?").first(),
                title=fake.sentence(nb_words=4),                  # SubTask title
                status=fake.random_element(elements=statuses),    # SubTask status
            )

        self.stdout.write(self.style.SUCCESS('SubTasks created.'))

    def create_notes(self, count):
        fake = Faker()

        for _ in range(count):
            Note.objects.create(
                task=Task.objects.order_by("?").first(),
                content=fake.paragraph(nb_sentences=2),           # Note content
            )

        self.stdout.write(self.style.SUCCESS('Notes created.'))
