from datetime import datetime, timedelta

import jwt
from django.contrib.auth.models import AbstractUser
from django.db import models

from Moove_Assessment.settings import SECRET_KEY


class User(AbstractUser):
    """
    The user model, basically for authentication
    """

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=1000)  # last a long time

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, SECRET_KEY, algorithm='HS256')

        return token

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        """
        return self._generate_jwt_token()


class Applicant(models.Model):
    """
    Applicant model
    """
    name = models.CharField(max_length=5)
    family_name = models.CharField(max_length=5)
    address = models.CharField(max_length=10)
    country_of_origin = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    hired = models.BooleanField(default=False)
