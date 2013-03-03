from tastypie import fields
from tastypie.api import Api
from tastypie.resources import ModelResource

from .models import Task, Update

class TaskResource(ModelResource):
    updates = fields.ToManyField('tasks.api.UpdateResource', 'update_set', null=True, full=True)
    class Meta:
        queryset = Task.objects.all()

class UpdateResource(ModelResource):
    task = fields.ForeignKey(TaskResource, 'task')
    message = fields.CharField(attribute="message")

    class Meta:
        queryset = Update.objects.all()


v1_api = Api(api_name='v1')
v1_api.register(TaskResource())
v1_api.register(UpdateResource())