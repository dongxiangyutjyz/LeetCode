from django.core.management.base import BaseCommand
from main.models import Twitter_User, Tweet
import tweepy
from afinn import Afinn
from django.utils import timezone
from datetime import datetime
import pytz
import requests
import json

class Command(BaseCommand):
	help = 'Scrapes Twitter for Trek tweets and stores them in database'
	
	url = "https://gender-api.com/get?name="
	key = "&key=946d64a0022933dec936848d4e68fb30c588ddd8e1d19292603b709ce0be2539"

	def handle(self, *args, **kwargs):
		auth = tweepy.OAuthHandler("amiKfJygvIY5PKHbrwYWp19YD","vOH7V77acZ6SFUMinAwFj47qWvOPmQgKy9CF8UQkWovEkqtoAp")
		auth.set_access_token("1088541921054806016-MCTqKdD0jS1QfcGGydiPvLgbLiO0Ar","1NCcStbqXWSOHlPvult1G2yN4gP2fhTCw16JwEj6DFlqB")

		api = tweepy.API(auth)
		af = Afinn(emoticons=True)

		class CustomStreamListener(tweepy.StreamListener):
			def on_status(self, status):
				url = "https://gender-api.com/get?name="
				key = "&key=946d64a0022933dec936848d4e68fb30c588ddd8e1d19292603b709ce0be2539"
				if 'stolen' not in status.text and 'star' not in status.text and 'Star' not in status.text and 'Stolen' not in status.text:
					try:
						tw_created_at = status.created_at.astimezone(pytz.utc) 
						tw_year = tw_created_at.strftime("%Y")
						tw_month = tw_created_at.strftime("%m")
						tw_day = tw_created_at.strftime("%d")
					except:
						tw_created_at = datetime.now()
						tw_year = tw_created_at.strftime("%Y")
						tw_month = tw_created_at.strftime("%m")
						tw_day = tw_created_at.strftime("%d")
					tw_id = status.id_str
					try:
						tw_text = status.extended_tweet['full_text']
					except:
						tw_text = status.text
					if hasattr(status, 'retweeted_status'):
						try:
							tw_text = status.retweeted_status.full_text
						except:
							tw_text = status.retweeted_status.text
					if(tw_text.split()[0] == 'RT'):
						tw_text = ' '.join(tw_text.split()[1:])
					wlist = tw_text.split()
					for word in wlist:
						if word[0] == '@':
							wlist.remove(word)
					tw_text = ' '.join(wlist)
					for word in wlist:
						if word.split(':')[0] == 'https':
							wlist.remove(word)
					tw_text = ' '.join(wlist)
					tw_user = status.user.id_str
					first_name = tw_user.split()[0]
					URL = url+str(first_name)+key
					response = requests.get(URL)
					response = response.json()
					tw_user_gender = response["gender"]
					print(tw_user_gender)
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
						#print(t)
						t.save()

					if not Twitter_User.objects.filter(t_id=user_id, t_screen_name=user_screen_name, t_user_name=user_name, t_user_location=user_location, t_user_description = user_description,t_user_gender = tw_user_gender):
						u = Twitter_User(t_id=user_id, t_screen_name=user_screen_name, t_user_name=user_name, t_user_location=user_location, t_user_description = user_description,t_user_gender = tw_user_gender)
						#print(u)
						u.save(u)

			def on_error(self, status_code):
				print >> sys.stderr, 'Encountered error with status code:', status_code
				return True # Don't kill the stream

			def on_timeout(self):
				print >> sys.stderr, 'Timeout...'
				return True # Don't kill the stream

		while(1):
			try:
				sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
				sapi.filter(track=['Trek bike', 'Trek bicycle', 'Trek bicycle corporation', 'Trek bikes', 'trekbikes', 'trekbike'])
			except:
				pass
			sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
			sapi.filter(track=['Trek bike', 'Trek bicycle', 'Trek bicycle corporation', 'Trek bikes', 'trekbikes', 'trekbike'])