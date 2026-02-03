from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment
from django.db.models import Q


# Home Page - Show all published posts
def home(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/home.html', context)

# Post Detail Page - Show single post with comments
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status='published')
    comments = post.comments.filter(approved=True)
    if request.method=="POST" and request.user.is_authenticated:
        form=CommentForm(request.POST)
        if form.is_valid():
           comment = form.save(commit=False)
           comment.post = post
           comment.author = request.user
           comment.save()
           messages.success(request, 'Your comment has been submitted and is awaiting approval.')
           return redirect('blog:post_detail', pk=pk)
    else:
        form = CommentForm()
        context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)

# Category Filter - Show posts by category
def category_posts(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.filter(category=category, status='published')
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'category': category,
        'categories': categories,
    }
    return render(request, 'blog/category_posts.html', context)

# Search Posts
def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        status='published'
    )
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'query': query,
        'categories': categories,
    }
    return render(request, 'blog/search_results.html', context)




from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, CommentForm

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('blog:login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('blog:home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'blog/login.html')

# User Logout
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('blog:home')

# Add Comment (update post_detail view)
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
            return redirect('blog:post_detail', pk=pk)
    return redirect('blog:post_detail', pk=pk)


@login_required
def user_profile(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    user_comments = Comment.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'user_posts': user_posts,
        'user_comments': user_comments,
    }
    return render(request, 'blog/profile.html', context)


from django.contrib.auth.decorators import login_required
from .forms import PostForm

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'published'
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog:home')
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'blog/create_post.html', context)


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts!')
        return redirect('blog:home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    context = {'form': form, 'post': post}
    return render(request, 'blog/edit_post.html', context)

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts!')
        return redirect('blog:home')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog:home')
    
    context = {'post': post}
    return render(request, 'blog/delete_confirm.html', context)
