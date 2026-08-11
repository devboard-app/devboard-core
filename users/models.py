import uuid

from django.db import models

# Create your models here.

class UserProfile(models.Model):

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MEMBER = 'member', 'Member'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, blank=True, default='')
    avatar = models.URLField(blank=True, default='')
    timezone = models.CharField(max_length=50, blank=True, default='Europe/Bucharest')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    last_active = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f'{self.email} ({self.role})'

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.email.split('@')[0]
        super().save(*args, **kwargs)

    @property
    def is_authenticated(self):
        return True
    