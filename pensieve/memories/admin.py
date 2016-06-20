from django.contrib import admin

from .models import Category, Prompt, Memory


class MemoryAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'title', 'creator')
    list_filter = ['created']


admin.site.register([Category, Prompt])
admin.site.register(Memory, MemoryAdmin)
