from django.contrib import admin

from .models import Account, Comment, Event, Idea, Idea_comment
admin.site.register(Account)
admin.site.register(Comment)
admin.site.register(Event)
admin.site.register(Idea)
admin.site.register(Idea_comment)
