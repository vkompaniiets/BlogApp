from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    tags = models.ManyToManyField(Tag, related_name='posts')
    title = models.CharField(max_length=256)
    text = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
