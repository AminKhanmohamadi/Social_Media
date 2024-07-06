from django.shortcuts import render ,redirect ,get_object_or_404
from django.views import View
from .models import Post, Comment , Like
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreatUpdateForm , CommentForm ,ReplyForm , PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.



class HomeView(View):
    form_class = PostSearchForm
    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request , 'home/index.html' , {'posts':posts , 'form':self.form_class})




class PostDetailView(View):
    form_class = CommentForm
    form_class_reply = ReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_ins = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    def get(self, request, *args, **kwargs ):
        comments = self.post_ins.post_comments.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.post_ins.user_can_like(request.user):
            can_like = True
        return render(request , 'home/detail.html' , {'posts':self.post_ins , 'comments':comments , 'form':self.form_class , 'reply_form':self.form_class_reply , 'can_like':can_like })

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_ins
            new_comment.save()
            messages.success(request, 'Your comment has been posted' , 'success')
            return redirect('home:detail' , self.post_ins.id , self.post_ins.slug)



class PostDeleteView(LoginRequiredMixin,View):

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request , 'Post deleted successfully' , 'success')
        else:
            messages.error(request , 'you can not delete this post' , 'danger')

        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostCreatUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post,pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, ' you can not update this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form  = self.form_class(instance=post)
        return render(request , 'home/update.html' , {'form':form})


    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST ,instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request , 'Post updated successfully' , 'success')
            return redirect('home:detail' , post.id , post.slug)



class CreatView(LoginRequiredMixin,View):
    form_class = PostCreatUpdateForm
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request , 'home/create.html' , {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request , 'Post created successfully' , 'success')
            return redirect('home:detail' , new_post.id , new_post.slug)



class PostAddReplyView(LoginRequiredMixin , View):
    form_class = ReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request , 'your reply submitted' , 'success')
        return redirect('home:detail', post.id , post.slug)



class PostLikeView(LoginRequiredMixin , View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        likes = Like.objects.filter(post=post , user=request.user)
        if likes.exists():
            messages.error(request , ' your have already liked this post' , 'danger')
        else:
            Like.objects.create(post=post , user=request.user)
            messages.success(request , ' you like this post' , 'success')
        return redirect('home:detail' ,post.id , post.slug)

