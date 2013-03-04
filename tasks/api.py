import datetime
import logging

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from django.conf.urls.defaults import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q

from tastypie import fields
from tastypie.api import Api
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from .models import Task, Update, Recipient, send_message


class TaskAuthorization(Authorization):

    def is_authorized(self, request, object=None):
        """
        Checks if the user is authorized to perform the request. If ``object``
        is provided, it can do additional row-level checks.

        Should return either ``True`` if allowed, ``False`` if not or an
        ``HttpResponse`` if you need something custom.
        """
        logging.error("checking!!!!!!! %s" % object)
        if request.user.is_authenticated():
            return True
        return False

    def apply_limits(self, request, object_list):
        if request.user.is_authenticated():
            return filter(lambda t: request.user in t.involved.all(), object_list)
        else:
            return []

    # def read_list(self, object_list, bundle):
    #     # This assumes a ``QuerySet`` from ``ModelResource``.
    #     logging.error("checking is able to read list")
    #     print "test" 
    #     raise
    #     return object_list.empty() #object_list.filter(Q(sender=bundle.request.user) | Q(involved__in=bundle.request.user))

    # def read_detail(self, object_list, bundle):
    #     # Is the requested object owned by the user?
    #     logging.error("checking is able to read")
    #     raise
    #     return bundle.obj.user == bundle.request.user

    # def create_list(self, object_list, bundle):
    #     # Assuming their auto-assigned to ``user``.
    #     logging.error("checking is able to read")
    #     return object_list

    # def create_detail(self, object_list, bundle):
    #     print "error"
    #     logging.error("checking is able to read")
    #     return bundle.obj.user == bundle.request.user

    # def update_list(self, object_list, bundle):
    #     logging.error("checking is able to read")
    #     allowed = []

    #     # Since they may not all be saved, iterate over them.
    #     for obj in object_list:
    #         if obj.user == bundle.request.user:
    #             allowed.append(obj)

    #     return allowed

    # def update_detail(self, object_list, bundle):
    #     return bundle.obj.user == bundle.request.user

    # def delete_list(self, object_list, bundle):
    #     # Sorry user, no deletes for you!
    #     raise Unauthorized("Sorry, no deletes.")

    # def delete_detail(self, object_list, bundle):
    #     raise Unauthorized("Sorry, no deletes.")


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        excludes = ["password", "is_staff", "is_superuser"]
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()

    def dehydrate(self, bundle):
        bundle.data['display_name'] = bundle.obj.username 
        return bundle


class TaskResource(ModelResource):
    sender = fields.ForeignKey(UserResource, 'sender', full=True)
    updates = fields.ToManyField('tasks.api.UpdateResource', 'update_set', null=True, full=True)
    recipients = fields.ToManyField('tasks.api.RecipientResource', 'recipient_set', null=True, full=True)

    class Meta:
        queryset = Task.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = SessionAuthentication()
        authorization = TaskAuthorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/respond%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('respond_task'), name="api_respond_task"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/complete%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('complete_task'), name="api_complete_task"),
        ]

    def respond_task(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        if request.GET.get('accepted', '') == 'true':
            obj.accept(request.user)
        else:
            obj.reject(request.user)

        return self.get_detail(request, ** kwargs)

    def complete_task(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(request=request, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")
        
        obj.complete(request.user)

        return self.get_detail(request, ** kwargs)


    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(TaskResource, self).build_filters(filters)
        # if "filter" in filters:
        #     filter_by = filters['filter']

        return orm_filters

    def get_object_list(self, request):
        object_list = super(TaskResource, self).get_object_list(request)

        filter_by = request.GET.get('filter', None)
        if filter_by == 'sent':
            object_list = object_list.filter(sender=request.user)
        elif filter_by == 'inbox':
            object_list = object_list.filter(Q(Q(recipient__to_user=request.user) & Q(recipient__status='PE')))
        elif filter_by == 'accepted':
            object_list = object_list.filter(Q(Q(recipient__to_user=request.user) & Q(recipient__status='AC')))
        elif filter_by == 'rejected':
            object_list = object_list.filter(Q(Q(recipient__to_user=request.user) & Q(recipient__status='RJ')))
        elif filter_by == 'completed':
            object_list = object_list.filter(Q(Q(recipient__to_user=request.user) & Q(recipient__status='CO')))
        elif filter_by == 'all':
            pass

        return object_list

    def dehydrate(self, bundle):
        bundle.data['is_to_group'] = bundle.obj.recipient_set.count() > 1 
        bundle.data['is_offer'] = bundle.obj.bounty and bundle.obj.bounty > 0
        return bundle

    # def hydrate_m2m(self, bundle):
    #     return bundle

    def hydrate_expire(self, bundle):
        expire = bundle.data['expire']
        if isinstance(expire, basestring) and expire.isdigit():
            expire = int(expire)

        if isinstance(expire, int):
            expire = datetime.datetime.now() + datetime.timedelta(days=int(expire))
            bundle.data['expire'] = expire

        return bundle

    def hydrate_bounty(self, bundle):
        bounty = bundle.data['bounty']
        if isinstance(bounty, basestring) and bounty.isdigit():
            bundle.data['bounty'] = int(bounty)

        return bundle


    # def hydrate_recipients(self, bundle):
    #     bundle.data['user'] = bundle.data['recipients']
    #     bundle.data['recipients'] = []
    #     return bundle

    def obj_create(self, bundle, request=None, **kwargs):

        bundle.data['sender'] = request.user

        try:
            new_bundle = super(TaskResource, self).obj_create(bundle, request, ** kwargs)
        except:
            logging.exception("error creating obj")
            return None

        usernames = bundle.data.get('users', [])
        if isinstance(usernames, basestring):
            usernames = usernames.split(',')
        
        try:
            new_bundle.obj.create(usernames=usernames)
        except User.DoesNotExist:
            raise BadRequest("user not found") # from tastypie.exceptions

        send_message({'action': 'create', 'model': 'task', 'id': new_bundle.obj.id})

        return new_bundle

class UpdateResource(ModelResource):
    task = fields.ForeignKey(TaskResource, 'task')
    message = fields.CharField(attribute="message")
    update_type = fields.CharField(attribute="update_type")

    class Meta:
        queryset = Update.objects.all()
        authentication = SessionAuthentication()

class RecipientResource(ModelResource):
    from_user = fields.ForeignKey(UserResource, 'from_user', full=True)
    to_user = fields.ForeignKey(UserResource, 'to_user', full=True)
    task = fields.ForeignKey(TaskResource, 'task')
    class Meta:
        queryset = Recipient.objects.all()
        authentication = SessionAuthentication()


v1_api = Api(api_name='v1')
v1_api.register(TaskResource())
v1_api.register(UpdateResource())
v1_api.register(UserResource())
