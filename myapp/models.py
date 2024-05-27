from django.db import models
from django.core.exceptions import ValidationError
from .models import Account
import json
import uuid
import random
import string

def generate_random_string(length):
    """Generate a random string of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class Account(models.Model):
    email_id = models.EmailField(unique=True)
    account_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    account_name = models.CharField(max_length=100, unique=True)
    app_secret_token = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        if not self.app_secret_token:
            self.app_secret_token = self._generate_app_secret_token()
        super().save(*args, **kwargs)

    def _generate_app_secret_token(self):
        return generate_random_string(length=20) 



class Destination(models.Model):
    account = models.ForeignKey(Account, related_name='destinations', on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    http_method = models.CharField(max_length=10)
    headers = models.JSONField()

    def clean(self):
        try:
            # Check if headers is a list, if yes, convert it to a dictionary
            if isinstance(self.headers, list):
                self.headers = dict(enumerate(self.headers))
            json.dumps(self.headers)  # Attempt to serialize headers to JSON
        except TypeError:
            raise ValidationError({'headers': 'Value must be valid JSON.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate JSON format before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Destination for {self.account.account_name}"