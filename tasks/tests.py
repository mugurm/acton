"""
"""
import logging

from django.test import TestCase

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

from .models import Task

class SimpleTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', email='user1@c.com')
        self.user2 = User.objects.create(username='user2', email='user2@c.com')
        self.user3 = User.objects.create(username='user3', email='user3@c.com')

    def test_task_actions(self):
        """
        Tests that 1 + 1 always equals 2.
        """

        t = Task(sender=self.user1, description="test task")
        t.create(usernames=[self.user2.username, self.user3.username])

        self.assertEqual(t.recipient_set.count(), 2)

        t.reject(self.user2)
        t.accept(self.user3)
        t.complete(self.user3)

        self.assertEqual(t.update_set.count(), 3)

