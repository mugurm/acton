from django.contrib.auth import get_user_model
User = get_user_model()

from jsonrpc import jsonrpc_method

from .models import Task

@jsonrpc_method('tasks.receive')
def task_receive(request, sender, users, description, expire=None, bounty=None):
    sender = User.get_or_create_remote_user(sender)   
    t = Task(sender=sender, description=description, expire=expire, bounty=bounty)
    t.create(users)
    return True

@jsonrpc_method('tasks.accept')
def task_accept(request, task_id, user):
    t = Task.objects.get(task_id=task_id)
    user = User.get_or_create_remote_user(user)
    t.accept(user)
    return True

@jsonrpc_method('tasks.reject')
def task_reject(request, task_id, user):
    t = Task.objects.get(task_id=task_id)
    user = User.get_or_create_remote_user(user)
    t.reject(user)
    return True

@jsonrpc_method('tasks.complete')
def task_complete(request, task_id, user):
    t = Task.objects.get(task_id=task_id)
    user = User.get_or_create_remote_user(user)
    t.complete(user)
    return True

