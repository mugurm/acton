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

QUOTE_STATUS = (
    ('PE', 'Pending'),
    ('AC', 'Accepted'),
    ('RE', 'Rejected'),
)

class Task(models.Model):
    sender = models.ForeignKey(User, related_name="created_tasks")
    involved = models.ManyToManyField(User) #all the people ever involve
    accepted_by = models.ForeignKey(User, related_name="taken_tasks", null=True, blank=True)
    task_id = models.CharField(max_length=36) #uuid
    description = models.TextField()
    status = models.CharField(max_length=2, choices=TASK_STATUS)
    archived = models.BooleanField(default=False)

    #terms
    expire = models.DateTimeField(null=True, blank=True)
    bounty = models.IntegerField(null=True, blank=True)
    can_change = models.BooleanField(default=True)
    can_forward = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s: %s" % (self.sender.email, self.description[:20])

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

class Recipient(models.Model):
    from_user = models.ForeignKey(User, related_name="tasks_sent")
    to_user = models.ForeignKey(User, related_name="tasks_received")
    task = models.ForeignKey(Task)

class Attachment(models.Model):
    task = models.ForeignKey(Task)
    file = models.FileField(upload_to="tasks/%Y/%m")

