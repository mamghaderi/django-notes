from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Tag(models.Model):
    # TODO: add created by and created time
    name = models.CharField(max_length=20, unique=True)


class Note(models.Model):
    title = models.CharField(max_length=100, null=False)
    body = models.TextField(max_length=10000, null=False)
    tags = models.ManyToManyField(Tag, related_name='note_tag', blank=True)
    public = models.BooleanField(default=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='snippets', on_delete=models.CASCADE)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
