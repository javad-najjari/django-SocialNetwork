from django.urls import path
from .views import HomeView, GlobalView, PostDetail, AddCommentView, ReplyingToComment



app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('global/', GlobalView.as_view(), name='global'),
    path('detail/<int:post_id>/', PostDetail.as_view(), name='detail'),
    path('comment/<int:post_id>', AddCommentView.as_view(), name='comment'),
    path('reply/<int:comment_id>', ReplyingToComment.as_view(), name='reply'),
]
