from django.shortcuts import redirect, render
from django.views import View
from accounts.models import Post, Comment
from .forms import AddCommentForm
from .mixins import LoginFirstMixin



class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            following = user.following.all()
            return render(request, 'home.html', {'following': following})
        else:
            return render(request, 'home.html')
            


class GlobalView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'global.html', {'posts': posts})


class PostDetail(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        context = {
            'post': post,
        }
        if request.user.is_authenticated:
            context['can_like'] = post.user_can_like(request.user)
            context['can_save'] = post.user_can_save(request.user)
        return render(request, 'post_detail.html', context)


class AddCommentView(LoginFirstMixin, View):
    form_class = AddCommentForm

    def get(self, request, post_id):
        return render(request, 'comment.html', {'form': self.form_class})

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        form = self.form_class(request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.post = post
            new_form.save()
            return redirect('home:detail', post.id)


class ReplyingToComment(LoginFirstMixin, View):
    form_class = AddCommentForm

    def get(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        return render(request, 'reply.html', {'form': self.form_class, 'comment': comment})
    
    def post(self, request, comment_id):
        form = self.form_class(request.POST)
        comment = Comment.objects.get(id=comment_id)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.post = comment.post
            new_form.real_reply = comment
            new_form.is_reply = True
            
            if not comment.is_reply:   # main comment
                new_form.reply = comment
            else:
                new_form.reply = comment.reply

            new_form.save()
            return redirect('home:detail', comment.post.id)
