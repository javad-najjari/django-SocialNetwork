from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    name = models.CharField(max_length=200)
    website = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/%Y/%m/%d', null=True, blank=True)
    private = models.BooleanField(default=False)

    def short_username(self):
        username_length = 8
        if len(self.username) > username_length:
            return f'{self.username[:username_length]}...'
        else:
            return self.username


class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.from_user} is following {self.to_user}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    image = models.ImageField(upload_to='post_images/%Y/%m/%d', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/%Y/%m/%d', null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)

    class Meta:
        ordering = ('-likes', '-saves', 'id')
    
    def __str__(self):
        return f'{self.user} created a post'
    
    def user_can_like(self, user):
        user_like = user.user_likes.filter(post=self).exists()
        return user_like

    def user_can_save(self, user):
        user_save = user.user_saves.filter(post=self).exists()
        return user_save
    
    def show_description(self):
        return self.description[:20]
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='comment_replies', null=True, blank=True)
    real_reply = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f'{self.user} -> {self.post}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return f'{self.user} liked {self.post}'



class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_saves')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_saves')
    
    def __str__(self):
        return f'{self.user} saved {self.post}'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')
    msg_content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def short_msg(self):
        return self.msg_content[:20]
    
    class Meta:
        ordering = ('-created',)
    