# your_app/models.py
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Video(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="videos")
    video_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField()
    like_count = models.PositiveIntegerField(null=True, blank=True)
    comment_count = models.PositiveIntegerField(null=True, blank=True)
    view_count = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
