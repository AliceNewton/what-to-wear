from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime, date, timedelta
import urllib2
import json
from items.models import Item


def index(request):
    return HttpResponse("Hello, world..")




def message(request):
    context = {
        "today":date.today()
    }
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
    outfits = Item.objects.filter(Q(rainproof=raining, smart=smartmeeting, lastworn__lte=date.today()-timedelta(12)) | Q(rainproof=raining, smart=smartmeeting, lastworn=None))
    print outfits
    context = {
        'outfits':outfits,
        'maxtemp':maxtemp,
        'raining':raining,
        "today":date.today(),
    }
    return render(request, 'outfit.html', context)


def chosenoutfit(request):
    mypk = request.POST['outfitid']
    outfit = Item.objects.get(pk=mypk)
    outfit.lastworn = date.today()
    outfit.save()
    context = {
        'outfit':outfit,
        'today':date.today(),
    }
    return render(request, 'outfitchosen.html', context)
