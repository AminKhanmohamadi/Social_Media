from django.urls import path
from .views import *


app_name = 'home'

urlpatterns = [
    path('' , HomeView.as_view() , name='home'),
    path('post/<int:post_id>/<slug:post_slug>/' , PostDetailView.as_view() , name='detail'),
    path('post/delete/<int:post_id>/' , PostDeleteView.as_view() , name='delete'),
    path('post/update/<int:post_id>/' , PostUpdateView.as_view() , name='update'),
    path('post/creat/' , CreatView.as_view() , name='creat'),
    path('reply/<int:post_id>/<int:comment_id>/' , PostAddReplyView.as_view() , name='reply'),
    path('like/<int:post_id>/' , PostLikeView.as_view() , name='like'),
]
