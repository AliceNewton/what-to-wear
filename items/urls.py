from django.conf.urls import patterns, url

from items import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^message$', views.message, name='message'),
    url(r'^weather$', views.weather, name='get_weather'),
    url(r'^chosenoutfit$', views.chosenoutfit, name='chosenoutfit')
)
