from django.conf.urls import url

from . import views

app_name = 'profiles'

# TODO - fix
urlpatterns = [
    url(r'^$', None, name='index'),
    url(r'^(?P<email>.+@.+)/$', None, name='detail'),
]
