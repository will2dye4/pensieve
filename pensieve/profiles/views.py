from django.shortcuts import render

from .forms import PensieveUserCreationForm


def index(request):
    return render(request, 'profiles/index.html', {'form': PensieveUserCreationForm()})
