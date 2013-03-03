from tastypie import fields
from tastypie.api import Api
from tastypie.resources import ModelResource

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from .models import Task, Update, Receipt

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()

    def dehydrate(self, bundle):
        bundle.data['display_name'] = bundle.obj.username 
        return bundle


class TaskResource(ModelResource):
    sender = fields.ForeignKey(UserResource, 'sender', full=True)
    updates = fields.ToManyField('tasks.api.UpdateResource', 'update_set', null=True, full=True)
    receipts = fields.ToManyField('tasks.api.ReceiptResource', 'receipt_set', null=True, full=True)

    class Meta:
        queryset = Task.objects.all()

    def dehydrate(self, bundle):
        bundle.data['is_to_group'] = bundle.obj.receipt_set.count() > 1 
        bundle.data['is_offer'] = bundle.obj.bounty and bundle.obj.bounty > 0
        return bundle

class UpdateResource(ModelResource):
    task = fields.ForeignKey(TaskResource, 'task')
    message = fields.CharField(attribute="message")
    update_type = fields.CharField(attribute="update_type")

    class Meta:
        queryset = Update.objects.all()

class ReceiptResource(ModelResource):
    from_user = fields.ForeignKey(UserResource, 'from_user', full=True)
    to_user = fields.ForeignKey(UserResource, 'to_user', full=True)
    task = fields.ForeignKey(TaskResource, 'task')
    class Meta:
        queryset = Receipt.objects.all()


v1_api = Api(api_name='v1')
v1_api.register(TaskResource())
v1_api.register(UpdateResource())
v1_api.register(UserResource())
