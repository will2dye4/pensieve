from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField('name', max_length=128, unique=True)
    created = models.DateTimeField('created time', auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                related_name='created_categories', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Prompt(models.Model):
    text = models.CharField('prompt', max_length=1024, unique=True)
    created = models.DateTimeField('created time', auto_now_add=True)
    updated = models.DateTimeField('updated time', auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                related_name='created_prompts', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='prompts', blank=True, null=True)

    def __str__(self):
        return self.text


class Memory(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.DO_NOTHING, related_name='responses', blank=True, null=True)
    title = models.CharField('title', max_length=256, blank=True)
    created = models.DateTimeField('created time', auto_now_add=True)
    updated = models.DateTimeField('updated time', auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                related_name='memories', blank=True, null=True)
    text = models.TextField('text')
    year = models.IntegerField('year', blank=True)
    month = models.IntegerField('month', blank=True)
    day = models.IntegerField('day', blank=True)
    location = models.CharField('location', max_length=256, blank=True)

    def __str__(self):
        name = ('"%s"' % self.title) if self.title else ('Response to "%s"' % self.prompt)
        return '%s by %s' % (name, self.creator.get_short_name())

    class Meta:
        unique_together = (('prompt', 'title', 'creator'),)
        verbose_name_plural = 'memories'
