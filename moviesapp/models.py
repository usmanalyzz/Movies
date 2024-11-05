from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Time(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    usman = models.CharField(max_length=2000, null=True)

class Movie(Time):
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    rating = models.FloatField()
    view_count = models.PositiveIntegerField(default=0)
    movie_category = models.CharField(max_length=100)
    reviews = models.TextField(blank=True, null=True)
    audience_count = models.PositiveIntegerField(default=0)
    banner_image_url = models.CharField(max_length=2000, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Video(Time):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='videos')
    video_url = models.CharField( max_length=2000 ,blank=True, null=True)

    def __str__(self):
        return f"Video for {self.movie.name}"


class Screenshot(Time):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='screenshots')
    image = models.CharField( max_length=2000 ,blank=True, null=True)

    def __str__(self):
        return f"Screenshot for {self.movie.name}"


class Comment(Time):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user_name = models.CharField(max_length=100)
    comment_text = models.TextField()

    def __str__(self):
        return f"Comment by {self.user_name} on {self.movie.name}"


class CommentLike(Time):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user} liked comment on {self.comment.movie.name}"


class TechSpec(Time):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='tech_specs')
    language = models.CharField(max_length=50)
    space = models.CharField(max_length=50)
    duration_hours = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return f"Tech Specs for {self.movie.name}"


class Like(Time):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user} liked {self.movie.name}"


class MovieInfo(Time):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_info')
    director_name = models.CharField(max_length=255)
    top_cast_names = models.TextField()
    summary = models.TextField()

    def __str__(self):
        return f"Info for {self.movie.name}"

