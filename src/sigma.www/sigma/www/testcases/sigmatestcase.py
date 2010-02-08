import unittest

from django.contrib.auth.models import User
from django.conf import settings

from sigma.www import workflow

class SigmaTestCase(unittest.TestCase):
    """Classe generic representant les testcase de sigma"""
    def setUp(self):
        try:
            self.user = User.objects.get(username=settings.ADMIN_LOGIN)
        except User.DoesNotExist:
            self.user = User(username=settings.ADMIN_LOGIN, 
                             password='get from settings.py')
            self.user.is_staff = True
            self.user.is_superuser = True
            self.user.save()
