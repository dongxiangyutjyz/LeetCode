import numpy as np
from celery import task
import got
import tweepy
from django.core.management.base import BaseCommand
from main.models import Twitter_User, Tweet
from afinn import Afinn
from django.utils import timezone
from datetime import datetime
import sys

@task(name='summary')
def send_import_summary():
	print('hello')
	#class Command(BaseCommand):
		#help = 'Scrapes Twitter for Trek tweets and stores them in database'
		#def handle(self, *args, **kwargs):
	auth = tweepy.OAuthHandler("amiKfJygvIY5PKHbrwYWp19YD","vOH7V77acZ6SFUMinAwFj47qWvOPmQgKy9CF8UQkWovEkqtoAp")
	auth.set_access_token("1088541921054806016-MCTqKdD0jS1QfcGGydiPvLgbLiO0Ar","1NCcStbqXWSOHlPvult1G2yN4gP2fhTCw16JwEj6DFlqB")
	api = tweepy.API(auth)
	af = Afinn(emoticons=True)
	class CustomStreamListener(tweepy.StreamListener):
		print('a')
		def on_status(self, status):
			print('b')
			if 'stolen' not in status.text:
				tw_created_at = status.created_at
				tw_year = tw_created_at.strftime("%Y")
				tw_month = tw_created_at.strftime("%m")
				tw_day = tw_created_at.strftime("%d")
				tw_id = status.id_str
				try:
					tw_text = status.extended_tweet.full_text
				except:
					tw_text = status.text
				if(tw_text.split()[0] == 'RT'):
					tw_text = ' '.join(tw_text.split()[1:])
				if(tw_text.split()[-1].split(':')[0] == 'https'):
					tw_text = ' '.join(tw_text.split()[:-1])
				tw_user = status.user.id_str
				try:
					tw_longitude = status.coordinates.coordinates[0]
					tw_latitude = status.coordinates.coordinates[1]
				except:
					tw_longitude = None
					tw_latitude = None
				tw_place = None #status.place.__dict__
				tw_retweet = status.retweeted
				try:
					tw_media = status.entities.media.__dict__
				except:
					tw_media = None
				try:
					tw_hashtags = status.entities.hashtags.__dict__
				except:
					tw_hashtags = None
				try:
					tw_psensitive = status.possibly_sensitive
				except:
					tw_psensitive = 0
				tw_score = af.score(tw_text)
				print(tw_score)
				tweet_user_user_name = status.user.name
				tweet_user_location = status.user.location
				user_id = status.user.id
				user_screen_name = status.user.screen_name
				user_name = status.user.name
				user_location = status.user.location
				user_description = status.user.description
			if not Tweet.objects.filter(tweet_created_at=tw_created_at, tweet_id=tw_id, tweet_text=tw_text, tweet_user=tw_user, tweet_longitude=tw_longitude, tweet_latitude=tw_latitude, tweet_place=tw_place, tweet_retweeted_status=tw_retweet, tweet_media=tw_media, tweet_hashtags=tw_hashtags, tweet_possibly_sensitive=tw_psensitive, tweet_score=tw_score, tweet_user_user_name=tweet_user_user_name, tweet_user_location=tweet_user_location, tweet_year=tw_year, tweet_month=tw_month, tweet_day=tw_day):
				t = Tweet(tweet_created_at=tw_created_at, tweet_id=tw_id, tweet_text=tw_text, tweet_user=tw_user, tweet_longitude=tw_longitude, tweet_latitude=tw_latitude, tweet_place=tw_place, tweet_retweeted_status=tw_retweet, tweet_media=tw_media, tweet_hashtags=tw_hashtags, tweet_possibly_sensitive=tw_psensitive, tweet_score=tw_score, tweet_user_user_name=tweet_user_user_name, tweet_user_location=tweet_user_location, tweet_year=tw_year, tweet_month=tw_month, tweet_day=tw_day)
				print(t)
				t.save()
			if not Twitter_User.objects.filter(t_id=user_id, t_screen_name=user_screen_name, t_user_name=user_name, t_user_location=user_location, t_user_description = user_description):
				u = Twitter_User(t_id=user_id, t_screen_name=user_screen_name, t_user_name=user_name, t_user_location=user_location, t_user_description = user_description)
				print(u)
				u.save(u)
		def on_error(self, status_code):
			print >> sys.stderr, 'Encountered error with status code:', status_code
			return True # Don't kill the stream

		def on_timeout(self):
			print >> sys.stderr, 'Timeout...'
			return True # Don't kill the stream
	sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
	sapi.filter(track=['Trek bike', 'Trek bicycle', 'Trek bicycle corporation', 'Trek bikes'])
	#tweetCriteria = got.manager.TweetCriteria().setQuerySearch('trek').setSince("2016-01-01").setMaxTweets(5)
	#tweets = got.manager.TweetManager.getTweets(tweetCriteria)
	#try:
		#print(tweet.text)
	#except:
		#print('a')
