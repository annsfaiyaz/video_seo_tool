# your_app/models.py
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    channel_id = models.CharField(max_length=255, null=True, blank=True)
    category_id = models.CharField(max_length=255)
    region = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.category_id


class Channel(models.Model):
    channel_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Video(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="videos")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="videos", null=True, blank=True)  # default set here
    video_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField()
    like_count = models.PositiveIntegerField(null=True, blank=True)
    comment_count = models.PositiveIntegerField(null=True, blank=True)
    view_count = models.PositiveIntegerField(null=True, blank=True)
    tags = models.ManyToManyField("Tag", related_name="videos", blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name