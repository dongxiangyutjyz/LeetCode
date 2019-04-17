from django.core.management.base import BaseCommand
from main.models import Twitter_User, Tweet
import os
from django.conf import settings
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

class Command(BaseCommand):
	help = 'Generates word cloud'

	def handle(self, *args, **kwargs):
		tweets = Tweet.objects.all().order_by('-tweet_created_at')[:200]

		big_tweet = ''

		for tweet in tweets:
			big_tweet = big_tweet + tweet.tweet_text

		# Create and generate a word cloud image:
		wordcloud = WordCloud().generate(big_tweet)

		# Save the image in the img folder:
		wordcloud.to_file(os.path.join(settings.BASE_DIR,'main/static/main/img/wordcloud.png'))

		# Display the generated image:
		plt.imshow(wordcloud, interpolation='bilinear')
		plt.axis("off")
		plt.show()

