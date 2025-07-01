from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from blog.forms import PostForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Q  

def post_home(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    return render(request, 'blog/post_home.html')

def post_list(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})
  
@login_required 
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form':form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form, 'post':post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
       return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_delete.html', {'post':post})    
    
def post_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully login")
            return redirect('post_list')
        else:
            messages.error(request, "You are invalid, Sorry")
    else:
        form = AuthenticationForm()
    return render(request, 'blog/post_login.html', {'form':form})


def post_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have created register successfully")
            return redirect('post_list')
        else:
            messages.success(request, "Registration failed")
    else:
        form = UserCreationForm()
    return render(request, 'blog/post_register.html', {'form':form})


def post_logout(request):
    logout(request)
    return redirect('post_home')