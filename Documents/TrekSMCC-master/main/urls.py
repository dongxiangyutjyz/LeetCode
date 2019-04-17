"""TrekSMCC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf.urls import url

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    url(r'^latest/$', views.get_latest, name="latest"),
    url(r'^feed/$', views.get_latest_feed, name="feed"),
    url(r'^sendTweet/$', views.send_tweet, name="sendTweet"),
    url(r'^cloudText/$', views.get_cloud_text, name="cloudText"),
    url(r'^getTweet/(?P<tweetid>[\s\S]*)/$', views.get_tweet, name="getTweet"),
    path("test/",views.ajaxtest,name="ajaxtest"),
]
