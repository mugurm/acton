from django.conf import settings
from django.db import models

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

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

QUOTE_STATUS = (
    ('PE', 'Pending'),
    ('AC', 'Accepted'),
    ('RE', 'Rejected'),
)

class Task(models.Model):
    creator = models.ForeignKey(User, related_name="created_tasks")
    taken_by = models.ForeignKey(User, related_name="taken_tasks", null=True, blank=True)
    to_users = models.ManyToManyField(User)
    task_id = models.CharField(max_length=36) #uuid
    title = models.CharField(max_length=64)
    status = models.CharField(max_length=2, choices=TASK_STATUS)
    description = models.TextField()
    expire = models.DateTimeField(null=True, blank=True)
    bounty = models.IntegerField(null=True, blank=True)
    archived = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s: %s" % (self.creator.email, self.title)


class Update(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    update_type = models.CharField(max_length=2, choices=UPDATE_TYPE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    quote = models.ForeignKey('tasks.Quote', null=True, blank=True)

class Quote(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    price = models.IntegerField()
    deliver_date = models.DateTimeField()
    details = models.TextField()
    status = models.CharField(max_length=2, choices=QUOTE_STATUS)

class Subscriber(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    role = models.CharField(max_length=2, choices=SUBSCRIBER_TYPE)

class Attachment(models.Model):
    task = models.ForeignKey(Task)
    file = models.FileField(upload_to="tasks/%Y/%m")

