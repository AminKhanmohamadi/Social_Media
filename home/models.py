from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='posts')
    body = models.TextField()
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.slug} - {self.updated}'


    def get_absolute_url(self):
        return reverse('home:detail' , args=[self.pk , self.slug])


    def likes_count(self):
        return self.likes_post.count()

    def user_can_like(self, user):
        user_like = user.likes_user.filter(post=self)
        if user_like.exists():
            return True
        return False

    class Meta:
        ordering = ['-created']




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name='post_comments')
    reply = models.ForeignKey('self' , on_delete=models.CASCADE , related_name='replies', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'




class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='likes_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name='likes_post')

    def __str__(self):
        return f'{self.user} - {self.post.slug}'


