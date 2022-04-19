from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    LikePost, ProfileView, ProfileView, Login, UserRegisterView, change_image, EditProfile,
    SavePost, LikedPosts, SavedPosts, link, FollowView, ListOfFollowers, ListOfFollowing,
    ListSearchUsers, ListMessages, MessageView,
    UserResetPasswordView, UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView
)



app_name = 'accounts'
urlpatterns = [

    path('profile/<username>', ProfileView.as_view(), name='profile'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),

    path('change-image/<int:user_id>', change_image, name='change-image'),
    path('edit-profile/<int:pk>', EditProfile.as_view(), name='edit_profile'),

    path('like/<int:post_id>', LikePost.as_view(), name='like_post'),
    path('save/<int:post_id>', SavePost.as_view(), name='save_post'),
    path('api/<int:post_id>', link, name='api_link'),
    
    path('liked-posts/', LikedPosts.as_view(), name='liked_posts'),
    path('saved-posts/', SavedPosts.as_view(), name='saved_posts'),

    path('follow/<username>', FollowView.as_view(), name='follow'),

    path('<username>/followers', ListOfFollowers.as_view(), name='followers_list'),
    path('<username>/following', ListOfFollowing.as_view(), name='following_list'),

    path('', ListSearchUsers.as_view(), name='search'),

    path('list-messages/', ListMessages.as_view(), name='list_messages'),
    path('message/<user1>_to_<user2>', MessageView.as_view(), name='message'),

    path('reset/', UserResetPasswordView.as_view(), name='reset_password'),
    path('reset-done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
