from django.conf.urls import url

from . import views

app_name = 'profiles'

# TODO - fix
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<email>.+@.+)/$', None, name='detail'),
]
