from django.db import models
from jsonfield import JSONField
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Twitter_User(models.Model):
	t_id = models.CharField(max_length=60)
	t_screen_name = models.CharField(max_length=20, null=True, blank=True)
	t_user_name = models.CharField(max_length=60)
	t_user_location = models.CharField(max_length=240, blank=True, null=True)
	t_user_description = models.TextField(blank=True, null=True)
	t_user_gender = models.CharField(max_length=20, blank=True, null=True, default='')

	def __str__(self):
		return self.t_user_name


class Tweet(models.Model):
	tweet_created_at = models.DateTimeField(max_length=60, blank=True)
	tweet_year = models.IntegerField(blank=True, null=True)
	tweet_month = models.IntegerField(blank=True, null=True)
	tweet_day = models.IntegerField(blank=True, null=True)
	tweet_id = models.CharField(max_length=60)
	tweet_text = models.TextField()
	tweet_user = models.CharField(max_length=60)
	tweet_longitude = models.FloatField(blank=True, null=True, default=None)
	tweet_latitude = models.FloatField(blank=True, null=True, default=None)
	tweet_place = JSONField(blank=True, default=None)
	tweet_retweeted_status = models.BooleanField(default=False, blank=True)
	tweet_media = JSONField(blank=True)
	tweet_hashtags = JSONField(blank=True)
	tweet_possibly_sensitive = models.BooleanField(default=False, blank=True)
	tweet_score = models.FloatField(blank=True, null=True)
	tweet_user_user_name = models.CharField(max_length=60, default='')
	tweet_user_location = models.CharField(max_length=240, blank=True, null=True, default='')

	def __str__(self):
		return self.tweet_text
