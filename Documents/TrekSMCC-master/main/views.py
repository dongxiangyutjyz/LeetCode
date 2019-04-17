from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet
from .models import Twitter_User
from django.utils import timezone
from datetime import datetime
from django.views.generic import ListView
from django.utils.timezone import localtime
import json
from datetime import datetime, timedelta, date
import pytz
import tweepy
import random
from nltk.corpus import stopwords
from dateutil.relativedelta import *
from pytz import common_timezones
from django.http import HttpResponseRedirect
from django.core import serializers
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


auth = tweepy.OAuthHandler("fwrSfG4uSUYv4iE38sMADRXRk", "i41PVv11Eh1wSue3aAhrucPE3Mcye5zRwALvMUikmO3KiwEMqh")
auth.set_access_token("1087756438288719873-qChEYx47VTjmU3POUIrK3WnZQK86NE", "VbyFkxUw8uRYWw3BCmj5EfGw7HxMqJa3yjQtmHZMt9HZp")

api = tweepy.API(auth)

central = pytz.timezone('US/Central')

# Create your views here.
def homepage(request):
	tw_created_at = datetime.today() + timedelta(days=1)
	tw_year = tw_created_at.strftime("%Y")
	tw_month = tw_created_at.strftime("%m")
	tw_day = tw_created_at.strftime("%d")
	day_score = []
	day_time = []
	week_score = []
	week_time = []
	month_score = []
	month_time = []
	year_score = []
	year_time = []

	one_day_ago = datetime.today().astimezone(central) - timedelta(days=1)
	tw_y = one_day_ago.strftime("%Y")
	tw_m = one_day_ago.strftime("%m")
	tw_d = one_day_ago.strftime("%d")
	day_tweets = Tweet.objects.filter(tweet_day=tw_d, tweet_month=tw_m, tweet_year=tw_y).order_by('tweet_created_at')
	while (one_day_ago.strftime("%d %m %H") != (datetime.today().astimezone(central).strftime("%d %m %H"))): 
		score = 0
		num = 0
		for t in day_tweets:
			if t.tweet_created_at.astimezone(central).strftime("%H") == one_day_ago.strftime("%H"): 
				score = score + t.tweet_score
				num = num + 1
		if num is 0:
			day_score.append(0)
			day_time.append(one_day_ago.strftime("%a %H:%M"))
			one_day_ago = one_day_ago + timedelta(hours=1)
		else:
			avg = score / num
			day_score.append(avg)
			day_time.append(one_day_ago.strftime("%a %H:%M"))
			one_day_ago = one_day_ago + timedelta(hours=1)

	#week tweets

	one_week_ago = datetime.today() - timedelta(days=7)
	week_tweets = Tweet.objects.filter(tweet_created_at__gte=one_week_ago).order_by('tweet_created_at')
	while (one_week_ago.strftime("%d %m") != (datetime.today() + timedelta(days=1)).strftime("%d %m")):
		score = 0
		num = 0
		for t in week_tweets:
			if t.tweet_created_at.astimezone(pytz.utc).strftime("%a") == one_week_ago.strftime("%a"): 
				score = score + t.tweet_score
				num = num + 1
		if num is 0:
			one_week_ago = one_week_ago + timedelta(days=1)
			continue
		else:
			avg = score / num
		week_score.append(avg)
		week_time.append(one_week_ago.strftime("%a"))
		one_week_ago = one_week_ago + timedelta(days=1)

	#month tweets
	last_month = datetime.today() - relativedelta(months=1)
	month_tweets = Tweet.objects.filter(tweet_created_at__gte=last_month).order_by('tweet_created_at')
	while (last_month.strftime("%d %m") != (datetime.today() + timedelta(days=1)).strftime("%d %m")):
		score = 0
		num = 0
		for t in month_tweets:
			if t.tweet_created_at.astimezone(pytz.utc).strftime("%d %m") == last_month.strftime("%d %m"): 
				score = score + t.tweet_score
				num = num + 1
		if num is 0:
			last_month = last_month + timedelta(days=1)
			continue
		else:
			avg = score / num
		month_score.append(avg)
		month_time.append(last_month.strftime("%b %d %Y"))
		last_month = last_month + timedelta(days=1)

	#year tweets
	last_year = datetime.today() - relativedelta(years=1)
	year_tweets = Tweet.objects.filter(tweet_created_at__gte=last_year).order_by('tweet_created_at')
	while (last_year.strftime("%m %Y") != (datetime.today() + relativedelta(months=1)).strftime("%m %Y")):
		score = 0
		num = 0
		for t in year_tweets:
			if t.tweet_created_at.astimezone(pytz.utc).strftime("%m %Y") == last_year.strftime("%m %Y"): 
				score = score + t.tweet_score
				num = num + 1
		if num is 0:
			last_year = last_year + relativedelta(months=1)
			continue
		else:
			avg = score / num
		year_score.append(avg)
		year_time.append(last_year.strftime("%B %Y"))
		last_year = last_year + relativedelta(months=1)

	users = list(Twitter_User.objects.values_list('t_user_gender'))
	locations = list(Tweet.objects.values_list('tweet_place'))

	return render(request = request,
		template_name='main/home.html',
		context = {"Twitter_Users":json.dumps({'data':users}), "tweet_place":json.dumps({'places':locations}), "today_data":day_score, "today_labels": day_time, "week_data":week_score, "week_labels":week_time, "month_data":month_score, "month_labels":month_time, "year_data":year_score, "year_labels":year_time})

def ajaxtest(request):
	print("helloworld")
	return homepage(request)

#create method that returns data in json (json python library)
#in java, use tie function to updata data , and rebuid the chart)

def get_latest(request):
	tw_created_at = datetime.today().astimezone(pytz.utc)
	tw_year = tw_created_at.strftime("%Y")
	tw_month = tw_created_at.strftime("%m")
	tw_day = tw_created_at.strftime("%d")
	latest_tweet_list = Tweet.objects.filter(tweet_day=tw_day, tweet_month=tw_month, tweet_year=tw_year).order_by('-tweet_created_at')
	if len(latest_tweet_list) >= 100:
		latest_tweet_list = latest_tweet_list[:100]
	if len(latest_tweet_list) > 0:
		oldest_date = latest_tweet_list[len(latest_tweet_list) - 1].tweet_created_at
	else:
		oldest_date = datetime.now().astimezone(pytz.utc)
	now = datetime.now().astimezone(pytz.utc)
	difference = int((now - oldest_date).total_seconds() / 60)

	## Granularity should be in hours or minutes
	scores = []
	times = []

	if difference > 100:
		hour = 0
		while (hour < 24):
			score_total = 0
			num = 0
			for tweet in latest_tweet_list:
				hour_string = str(hour)
				if hour < 10:
					hour_string = "0" + hour_string
				if hour_string == tweet.tweet_created_at.astimezone(central).strftime("%H"):
					score_total += tweet.tweet_score
					num += 1
				else:
					continue   
			if num > 0:
				scores.append(score_total / num)
				times.append(str((hour % 12) + 1) + ":00")
			hour += 1


	else:
		newest_date = latest_tweet_list[0].tweet_created_at
		minute_difference = (newest_date - oldest_date).total_seconds() / 60
		minute = 0

		while (minute <= minute_difference):

			score_total = 0
			num = 0
			for tweet in latest_tweet_list:
				if int (((newest_date - tweet.tweet_created_at).total_seconds() / 60)) == minute:
					score_total += tweet.tweet_score
					num += 1
				else:
					continue
			if num > 0:
				scores.append(score_total / num)
				hour_string = str(round((int(oldest_date.astimezone(central).strftime("%H")) - minute) / 60))
				minute_string = str(round(minute % 60))
				if len(minute_string) == 1:
					minute_string = "0" + minute_string

				times.append(hour_string + ":" + minute_string)
			minute += 1


	return_object = {}
	return_object["scores"] = scores
	return_object["times"] = times
	return HttpResponse(json.dumps(return_object), content_type='application/json')

def get_latest_feed(request):
	latest_tweet_list = Tweet.objects.order_by('-tweet_created_at')[:5]

	tweetText = []
	tweetCreatedAt = []
	userName = []
	tweetLocation = []
	tweetID = []
	tweetUserDisplay = []

	for tweet in latest_tweet_list:
		tweetText.append(tweet.tweet_text)
		tweetCreatedAt.append(tweet.tweet_created_at.strftime("%a %m/%d/%Y, %H:%M %p"))
		user = Twitter_User.objects.get(t_user_name=tweet.tweet_user_user_name)
		userName.append(user.t_screen_name)
		tweetLocation.append(tweet.tweet_user_location)
		tweetID.append(tweet.tweet_id)
		tweetUserDisplay.append(tweet.tweet_user_user_name)

	return_object = {}
	return_object["tweetText"] = tweetText
	return_object["tweetCreatedAt"] = tweetCreatedAt
	return_object["userName"] = userName
	return_object['tweetLocation'] = tweetLocation
	return_object["tweetID"] = tweetID
	return_object["tweetUserDisplay"] = tweetUserDisplay
	return HttpResponse(json.dumps(return_object), content_type='application/json')

def send_tweet(request):
	print("hi")
	data=json.loads(request.body.decode("utf-8"))
	print(data)
	tweetID = data['tweetID']
	tweetTextToSend = data['tweetTextToSend']
	print(tweetTextToSend, tweetID)
	s = api.update_status(tweetTextToSend, tweetID)
	return_object = {}
	return_object['result'] = 'success'
	return HttpResponse(json.dumps(return_object), content_type='application/json')

def get_tweet(request, tweetid):
	tid_list = tweetid.split(" ")
	tid = tid_list[0]
	tuid = ('').join(tid_list[1:])
	return_object = {}
	return_object['screenName'] = tuid
	return_object['tweetID'] = tid
	return HttpResponse(json.dumps(return_object), content_type='application/json')

def get_cloud_text(request):
	latest_tweet_list = Tweet.objects.order_by('-tweet_created_at')[:200]
	stop = stopwords.words('english')
	dataDict = {}
	for tweet in latest_tweet_list:
		stringWordList = tweet.tweet_text.split(" ")
		for word in stringWordList:
			if word not in stop:
				if word in dataDict.keys():
					dataDict[word] += 1
				else:
					dataDict[word] = 1

	return_object = {}
	return_list = []
	for word, value in dataDict.items():
		newDict = {}
		newDict["word"] = word
		newDict["value"] = value
		return_list.append(newDict)
	
	return_object["cloudText"] = return_list[:125]
	return HttpResponse(json.dumps(return_object), content_type='application/json')