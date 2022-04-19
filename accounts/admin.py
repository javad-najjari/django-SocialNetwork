from django.contrib import admin
from .models import User, Follow, Post, Comment, Like, Save, Message




admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Save)



class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'likes', 'saves', 'show_description')
admin.site.register(Post, PostAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'reciever', 'short_msg', 'created')
admin.site.register(Message, MessageAdmin)
