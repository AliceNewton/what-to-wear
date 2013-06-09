from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, date, timedelta
import urllib2
import json
from items.models import Item


def index(request):
    return HttpResponse("Hello, world. ")




def message(request):
#    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {}
    return render(request, 'meetingq.html', context)


def weather(request):
    today = date.today()
    url = 'http://free.worldweatheronline.com/feed/weather.ashx?key=a6d8eaaef8203121120909&q=SW7&num_of_days=1&format=json'
    json_raw = urllib2.urlopen(url).read()
    weatherdata = json.loads(json_raw)
    maxtemp = weatherdata['data']['weather'][0]['tempMaxC']
    maxtemp = int(maxtemp)
    weatherDesc = weatherdata['data']['weather'][0]['weatherDesc'][0]['value']
    raining = 'rain' in weatherDesc

    # get calendar information
    qanswer = request.REQUEST['qanswer']
    smartmeeting = (qanswer == 'Yes')

    # pick outfit with appropriate criteria
#    outfit = query_db("SELECT * FROM items WHERE rainproof=? AND smart=? AND DATE(lastworn) <= DATE('now', 'weekday 0', '-18 days')", (raining, smartmeeting))
    outfits = Item.objects.filter(rainproof=raining, lastworn__lte=date.today()-timedelta(18))
    context = {
        ''
    }
    return render(request, 'outfit.html', context_instance=context)
