from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from blog.forms import PostForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})
  

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


def post_edit(request, pk):
    post = Post.objects.all(Post, pk=pk)
    if post.user != request.user:
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form':form})
        
            
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user:
        post.delete()
    return redirect('post_list')


def post_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            post = form.save()
            login(request, post)
            messages.success(request, "You have successfully logged-in")
            return redirect('')
        else:
            messages.error(request, "You are invalid sorry")
    else:
        form = AuthenticationForm()
    return render(request, 'blog/post_login.html', {'form':form})

def post_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            post = form.save()
            login(request, post)
            messages.success(request, "You have register successfully")
            return redirect('')
    else:
        form = UserCreationForm()
    return render(request, 'blog/post_register.html', {'form':form})