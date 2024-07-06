from django.shortcuts import render ,redirect , get_object_or_404
from django.views import View
from .forms import UserRegisterForm ,UserLoginForm , EditUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
# Create your views here.

class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request , *args, **kwargs)
    def get(self, request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            messages.success(request, 'Account created successfully' , 'success')
            return redirect('home:home')
        return render(request , self.template_name , {'form':form})


class UserLoginView(View):
    form_class = UserLoginForm
    templates_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request , *args , **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request , *args, **kwargs)
    def get(self, request):
        form = self.form_class()
        return render(request , self.templates_name, {'form':form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'] , password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in' , 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'Invalid username or password' , 'error')
        return render(request , self.templates_name, {'form':form})


class UserLogoutView(LoginRequiredMixin,View):

    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out' , 'success')
        return redirect('home:home')



class UserProfileView(LoginRequiredMixin , View):
    def get(self, request , user_id):
        is_following = False
        user = get_object_or_404(User,pk=user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user , to_user=user)
        if relation.exists():
            is_following = True
        return render(request , 'account/profile.html' , {'user':user , 'posts':posts , 'is_following':is_following})



class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/passwordreset.html'
    success_url = reverse_lazy('account:reset_password_done')
    email_template_name = 'account/password_reset_email.html'



class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'



class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

class UserFollowView(LoginRequiredMixin, View):
    def get(self, request , user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user , to_user=user)
        if relation.exists():
            messages.error(request , 'you are already following' , 'success')
        else:
            Relation.objects.create(from_user=request.user , to_user=user)
            messages.success(request , 'you are now following ' , 'success')
        return redirect('account:profile' , user.id)


class UserUnfollowView(LoginRequiredMixin, View):

    def get(self , request , user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user , to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request , 'شما با موفقیت unfollow کردید')
        else:
            messages.error(request , 'شما این شخص را فالو نکرده اید')
        return redirect('account:profile' , user.id)



class EditUserView(LoginRequiredMixin , View):
    form_class = EditUserForm
    def get(self, request):
        form =self.form_class(instance=request.user.profile , initial={'email':request.user.email})
        return render(request , 'account/edit_profile.html' , {'form':form})

    def post(self, request):
        form = self.form_class(request.POST , instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Your account has been updated' , 'success')
        return redirect('account:profile' , request.user.id)
