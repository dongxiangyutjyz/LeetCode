from django.core.management.base import BaseCommand
from main.models import Twitter_User, Tweet
import tweepy
from afinn import Afinn
from django.utils import timezone
from datetime import datetime, timedelta, date
import GetOldTweets3 as got3
import pytz

class Command(BaseCommand):
	help = 'Scrapes Twitter for Trek tweets and stores them in database'

	def handle(self, *args, **kwargs):
		tweetCriteria = got3.manager.TweetCriteria().setQuerySearch('Trek bike OR Trek bicycle OR Trek bicycle corporation OR Trek bikes OR trekbikes OR trekbike').setSince("2018-01-01").setUntil("2019-01-01").setMaxTweets(2000)
		tweets = got3.manager.TweetManager.getTweets(tweetCriteria)
		af = Afinn(emoticons=True)

		for tweet in tweets:
			if 'stolen' not in tweet.text and 'star' not in tweet.text and 'Star' not in tweet.text and 'Stolen' not in tweet.text and 'Ad' not in tweet.text:
				tw_created_at = tweet.date
				tw_year = tw_created_at.strftime("%Y")
				tw_month = tw_created_at.strftime("%m")
				tw_day = tw_created_at.strftime("%d")
				try:
					tw_id = tweet.id_str
				except:
					tw_id = str(tweet.id)
				try:
					tw_text = tweet.extended_tweet['full_text']
				except:
					tw_text = tweet.text
				try:
					if tw_text.split()[0] == 'RT':
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
				except:
					continue
				try:
					tw_user = tweet.username
				except:
					tw_user = None
				
				if tweet.retweets > 0:
					tw_retweet = 1
				else:
					tw_retweet = 0
				tw_score = af.score(tw_text)
				tweet_user_user_name = tweet.username
				tweet_user_location = tweet.geo
				user_id = tweet.author_id
				user_name = tweet.username
				user_location = tweet.geo
				tw_hashtags = tweet.hashtags

				if not Tweet.objects.filter(tweet_created_at=tw_created_at, tweet_id=tw_id, tweet_text=tw_text, tweet_user=tw_user, tweet_longitude=None, tweet_latitude=None, tweet_place=None, tweet_retweeted_status=tw_retweet, tweet_media=None, tweet_hashtags=tw_hashtags, tweet_possibly_sensitive=0, tweet_score=tw_score, tweet_user_user_name=tweet_user_user_name, tweet_user_location=tweet_user_location, tweet_year=tw_year, tweet_month=tw_month, tweet_day=tw_day):
					t = Tweet(tweet_created_at=tw_created_at, tweet_id=tw_id, tweet_text=tw_text, tweet_user=tw_user, tweet_longitude=None, tweet_latitude=None, tweet_place=None, tweet_retweeted_status=tw_retweet, tweet_media=None, tweet_hashtags=tw_hashtags, tweet_possibly_sensitive=0, tweet_score=tw_score, tweet_user_user_name=tweet_user_user_name, tweet_user_location=tweet_user_location, tweet_year=tw_year, tweet_month=tw_month, tweet_day=tw_day)
					t.save()
					print("saved")

				if not Twitter_User.objects.filter(t_id=user_id, t_screen_name=None, t_user_name=user_name, t_user_location=user_location, t_user_description = None):
					u = Twitter_User(t_id=user_id, t_screen_name=None, t_user_name=user_name, t_user_location=user_location, t_user_description = None)
					u.save(u)