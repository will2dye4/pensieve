from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_categories', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Prompt(models.Model):
    text = models.CharField(max_length=1024, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_prompts', null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='prompts', null=True)

    def __str__(self):
        return self.text


class Memory(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.DO_NOTHING, related_name='responses', null=True)
    title = models.CharField(max_length=256, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='memories', null=True)
    text = models.TextField()
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    location = models.CharField(max_length=256, null=True)

    def __str__(self):
        name = ('"%s"' % self.title) if self.title else ('Response to "%s"' % self.prompt)
        return '%s by %s' % (name, self.creator.username)

    class Meta:
        unique_together = (('prompt', 'title', 'creator'),)
        verbose_name_plural = 'memories'

