from django.contrib import admin
from .models import Post,Likes,User,Follower

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=("post","post_date","user")

admin.site.register(Post,PostAdmin)

class LikesAdmin(admin.ModelAdmin):
    list_display=("liked_post","liked_by")
admin.site.register(Likes,LikesAdmin)


class FollowerAdmin(admin.ModelAdmin):
    list_display=("user","follower")

admin.site.register(Follower,FollowerAdmin)

admin.site.register(User)