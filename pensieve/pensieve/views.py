from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render

from profiles.forms import PensieveUserCreationForm
from profiles.models import PensieveUser


# The literal name of the HTTP Referrer header. The typo below in 'referrer' is intentional.
REFERRER = 'HTTP_REFERER'


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '')
        try:
            PensieveUser.objects.get(email=email)
        except PensieveUser.DoesNotExist:
            error = 'You have entered an invalid email or password. Please check your credentials and try again.'
        else:
            user = auth.authenticate(email=email, password=request.POST.get('password'))
            if user is None:
                error = 'You have entered an invalid email or password. Please check your credentials and try again.'
            elif not user.is_active:
                error = 'Your account has been disabled. Please contact an administrator to have it re-enabled.'
            else:
                auth.login(request, user)
                return HttpResponseRedirect(_get_redirect_destination(request.META[REFERRER]))
    else:
        email = ''

    return render(request, 'pensieve/login.html', {'email': email, 'error': error})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = PensieveUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('Created user', user.id, 'with email', user.email)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = PensieveUserCreationForm()
    return render(request, 'pensieve/register.html', {'form': form})


def _get_redirect_destination(referrer):
    """Find and return the 'next' parameter from the HTTP Referrer header, if present.

    Required parameters:
        - referrer  =>  the content of the HTTP Referrer header, as a string

    """
    index = referrer.find('?')
    if index > -1:
        params = QueryDict(referrer[index + 1:])
        if 'next' in params:
            return params['next']
    return reverse('index')
