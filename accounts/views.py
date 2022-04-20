from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import UpdateView
from django.contrib.auth import authenticate, login, views as auth_views
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, ChangeImageForm, MessageForm, UserLoginForm
from accounts.models import User
from django.contrib import messages
from .mixins import EditAccessMixin
from .models import Like, Save, Post, Follow, Message
from home.mixins import LoginFirstMixin
from django.db.models import Q






class ProfileView(View):
    def get(self, request, username):
        form = UserRegistrationForm
        user = User.objects.get(username=username)
        user_auth = request.user
        if request.user.is_authenticated:
            is_following = Follow.objects.filter(from_user=user_auth, to_user=user).exists()
        else:
            is_following = 'nobody'
        return render(request, 'profile.html', {'form': form, 'user': user, 'is_following': is_following})


class Login(View):
    form_class = UserLoginForm
    template_name = 'login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)


    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(image=cd['image'], email=cd['email'], username=cd['username'], name=cd['name'], 
            bio=cd['bio'], website=cd['website'], password=cd['password1'])
            messages.success(request, 'you registered successfully', 'success')
            return redirect('home:home')
        else:
            messages.error(request, 'something is wrong', 'danger')
            return render(request, self.template_name, {'form': form})



def change_image(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        form = ChangeImageForm(request.POST)
        if form.is_valid():
            user.image = request.FILES['image']
            user.save()
        else:
            messages.error(request, 'something is wrong', 'error')

    return redirect('accounts:profile', user.username)


class EditProfile(EditAccessMixin, UpdateView):
    model = User
    fields = ('username', 'name', 'bio', 'website', 'private')
    template_name = 'edit-profile.html'
    success_url = reverse_lazy('home:home')


class LikePost(LoginFirstMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user
        is_like = Like.objects.filter(post=post, user=user)
        if not is_like.exists():
            Like.objects.create(post=post, user=user)
            post.likes += 1
        else:
            is_like.delete()
            post.likes -= 1
        post.save()
        return redirect('home:detail', post.id)


class SavePost(LoginFirstMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user
        is_save = Save.objects.filter(post=post, user=user)
        if not is_save.exists():
            Save.objects.create(post=post, user=user)
            post.saves += 1
        else:
            is_save.delete()
            post.saves -= 1
        post.save()
        return redirect('home:detail', post.id)


class LikedPosts(View):
    def get(self, request):
        user = request.user
        posts = user.user_likes.all()
        title = 'Posts you liked'
        return render(request, 'saved-liked-posts.html', {'posts': posts, 'title': title})


class SavedPosts(View):
    def get(self, request):
        user = request.user
        posts = user.user_saves.all()
        title = 'Posts you saved'
        return render(request, 'saved-liked-posts.html', {'posts': posts, 'title': title})


class FollowView(LoginFirstMixin, View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        user_auth = request.user
        is_following = Follow.objects.filter(from_user=user_auth, to_user=user)
        if user == user_auth:
            messages.error(request, "you can't follow yourself", 'danger')
            return redirect('accounts:profile', user)
        if not is_following.exists():
            Follow.objects.create(from_user=user_auth, to_user=user)
        else:
            is_following.delete()
        
        return redirect('accounts:profile', user)


class ListOfFollowers(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        follows = user.followers.all()
        title = 'Followers'
        context = {
            'follows': follows, 'title': title
            }
        return render(request, 'list-users.html', context)


class ListOfFollowing(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        followings = user.following.all()
        title = 'Following'
        context = {
            'followings': followings, 'title': title
            }
        return render(request, 'list-users.html', context)
    

class ListSearchUsers(View):
    def get(self, request):
        context = {
            'users': User.objects.filter(username__contains = request.GET['search']).order_by('username'),
            'word': request.GET['search'],
        }
        if len(context['users']) == 0:
            context['users'] = User.objects.filter(bio__contains = request.GET['search'])
        return render(request, 'list-search-users.html', context)


class ListMessages(LoginFirstMixin, View):
    def get(self, request):
        msgs = Message.objects.filter(Q(sender=request.user) | Q(reciever=request.user)).order_by('-created')
        all_users = []
        for msg in msgs:
            if msg.sender != request.user:
                all_users.append(msg.sender.username)
            else:
                all_users.append(msg.reciever.username)

        users = User.objects.filter(username__in = all_users)
        return render(request, 'list_messages.html', {'users': users})


class MessageView(LoginFirstMixin, View):
    form_class = MessageForm
    def get(self, request, user1, user2):
        form = self.form_class
        global user
        if request.user.username != user1:
            user = User.objects.get(username=user1)
        elif request.user.username != user2:
            user = User.objects.get(username=user2)
        msgs = Message.objects.filter((Q(sender=request.user) & Q(reciever=user)) | (Q(sender=user) & Q(reciever=request.user))).order_by('created')
        return render(request, 'message.html', {'msgs': msgs, 'user': user, 'form': form})
    
    def post(self, request, user1, user2):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Message.objects.create(sender=request.user, reciever=user, msg_content=cd['msg_content'])
        return redirect('accounts:message', request.user.username, user.username)


# Reset Password
class UserResetPasswordView(auth_views.PasswordResetView):
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'password_reset_email.html'

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

