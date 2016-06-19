from django.contrib import admin

from .models import Category, Prompt, Memory


admin.site.register([Category, Prompt, Memory])
