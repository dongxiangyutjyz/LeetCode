from django.core.management.base import BaseCommand
from main.models import Twitter_User, Tweet
import os
from django.conf import settings
import numpy as np
import pandas as pd
from os import path
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime

class Command(BaseCommand):
	help = 'Creates 24 hour plot of sentiment vs time'

	def handle(self, *args, **kwargs):
		tweets = Tweet.objects.all().order_by('-tweet_created_at')[:200]

		sentiment_values = [[tweet.tweet_score, tweet.tweet_created_at] for tweet in tweets if tweet.tweet_created_at.date() == datetime.today().date()]

		sentiment_df = pd.DataFrame(sentiment_values, columns=['Tweet Sentiment', 'Time'])

		sentiment_df.plot(kind='line', x='Time', y='Tweet Sentiment', color='red', figsize=(10,5))
		plt.xlabel("Time")
		plt.ylabel("Tweet Sentiment")
		#plt.show()

				# Save the image in the img folder:
		plt.savefig(os.path.join(settings.BASE_DIR,'main/static/main/img/24hour.png'), bbox_inches='tight')
