from django.conf import settings
from django.db import models

TASK_STATUS = (
    ('PE', 'Pending'),
    ('AC', 'Accepted'),
    ('RJ', 'Rejected'),
    ('CO', 'Completed'),
)

UPDATE_TYPE = (
    ('AC', 'Accept'),
    ('RJ', 'Reject'),
    ('QO', 'Quote'),
    ('PR', 'Progress'),
    ('CO', 'Complete'),
    ('ME', 'Message'),
)

SUBSCRIBER_TYPE = (
    ('CR', 'Creator'),
    ('AS', 'Assigned'),
    ('WA', 'Watcher')
)

class Task(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_tasks")
    taken_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="taken_tasks")
    task_id = models.CharField(max_length=36) #uuid
    title = models.CharField(max_length=64)
    status = models.CharField(max_length=2, choices=TASK_STATUS)
    description = models.TextField()
    expire = models.DateTimeField(null=True, blank=True)
    bounty = models.IntegerField(null=True, blank=True)
    archived = models.BooleanField(default=False)

class Update(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    update_type = models.CharField(max_length=2, choices=UPDATE_TYPE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    quote = models.ForeignKey('tasks.Quote', null=True, blank=True)

class Quote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    task = models.ForeignKey(Task)
    price = models.IntegerField()
    deliver_date = models.DateTimeField()
    details = models.TextField()

class Subscriber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    task = models.ForeignKey(Task)
    role = models.CharField(max_length=2, choices=SUBSCRIBER_TYPE)

class Attachment(models.Model):
    task = models.ForeignKey(Task)
    file = models.FileField(upload_to="tasks/%Y/%m")

