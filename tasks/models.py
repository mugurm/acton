import logging
import uuid

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

RECIPIENT_STATUS = (
    ('PE', 'Pending'),
    ('AC', 'Accepted'),
    ('RJ', 'Rejected'),
    ('CL', 'Closed'),
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

from firebase import firebase
fbapp = firebase.FirebaseApplication('https://acton.firebaseio.com', None)

def send_message(msg):
    return fbapp.post('/messages', msg)

class Error(Exception):
    pass

class UnauthorizedError(Error):
    pass

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

    class Meta:
        ordering = ("-id",)

    def __unicode__(self):
        if self.sender and self.description:
            return u"%s: %s" % (self.sender.email, self.description[:20])
        else:
            return ""

    def update_involved(self):
        self.involved.clear()
        self.involved.add(self.sender)
        for recipient in self.recipient_set.all():
            self.involved.add(recipient.to_user)

    def save(self, * args, ** kwargs):
        if self.pk:
            self.update_involved()

        super(Task, self).save(* args, ** kwargs)

    def create(self, usernames=None, users=None):
        """
            Create tasks, does the final save and creates the Recipient objects
        """
        self.task_id = "%s" % uuid.uuid1()
        self.save()

        if users is None:
            users = []

        for user in usernames:
            user = user.strip()
            if user.startswith('+'):
                user = user[1:]

            if "@" not in user:
                users.append(User.objects.get(username=user))
            else:
                raise NotImplementedError()

        for u in users:
            Recipient(from_user=self.sender, to_user=u, task=self).save()

        self.save()


    def accept(self, user):
        logging.info("accepted")
        try:
            recipient = self.recipient_set.filter(to_user=user).get()
        except Recipient.DoesNotExist:
            raise UnauthorizedError("user is not able")

        if self.status in ['CO', 'RJ']:
            raise Error('Task not in pending status')

        self.status = 'AC'
        self.accepted_by = user
        self.save()
        
        for recipient in self.recipient_set.all():
            recipient.status = 'CL'
            recipient.save()
        recipient.status = 'AC'
        recipient.save()
        
        Update(user=user, task=self, update_type='AC', message='').save()

        send_message({'action': 'accept', 'model': 'task', 'id': self.id})
        return self

    def reject(self, user):
        logging.info("rejected")
        try:
            recipient = self.recipient_set.filter(to_user=user).get()
        except Recipient.DoesNotExist:
            raise UnauthorizedError("user is not able")

        if recipient.status != 'PE':
            raise Error('Task not in pending status')

        recipient.status = 'RJ'
        recipient.save()

        Update(user=user, task=self, update_type='RE', message='').save()

        total_recipients =self.recipient_set.count()
        rejected_recipients =self.recipient_set.filter(status='RJ').count()
        if self.status == 'PE' and total_recipients == rejected_recipients:
            self.status = 'RJ'
            self.save()

        send_message({'action': 'reject', 'model': 'task', 'id': self.id})

        return self

    def complete(self, user):
        logging.info("completed")
        try:
            recipient = self.recipient_set.filter(to_user=user).get()
        except Recipient.DoesNotExist:
            raise UnauthorizedError("user is not able")

        if recipient.status != 'AC':
            raise Error('Task not in accepted status')

        recipient.status = 'CO'
        recipient.save()

        Update(user=user, task=self, update_type='CO', message='').save()

        self.status = 'CO'
        self.save()

        send_message({'action': 'complete', 'model': 'task', 'id': self.id})

        return self


class Update(models.Model):
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    update_type = models.CharField(max_length=2, choices=UPDATE_TYPE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    quote = models.ForeignKey('tasks.Quote', null=True, blank=True)

    def __unicode__(self):
        return u"f:%s t:%s s:%s" % (self.user, self.task, self.update_type)

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
    status = models.CharField(max_length=2, choices=RECIPIENT_STATUS, default='PE')

    def __unicode__(self):
        return u"f:%s t:%s s:%s" % (self.from_user, self.to_user, self.status)

class Attachment(models.Model):
    task = models.ForeignKey(Task)
    file = models.FileField(upload_to="tasks/%Y/%m")

