from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment, Story, UserProfile, StoryView
from .forms import UserRegisterForm, PostForm, UserUpdateForm, UserProfileForm, StoryForm
from django.contrib.auth.models import User

def home(request):
    posts = Post.objects.select_related('author').order_by('-created_at')
    stories = Story.objects.select_related('user', 'user__profile').order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts, 'stories': stories})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created for {form.cleaned_data.get("username")}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request, 'Post created successfully.')
            return redirect('home')
        messages.error(request, 'Post could not be created. Please fix the errors below.')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You can't edit someone else's post!")
        return redirect('home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', pk=post.pk)
        messages.error(request, 'Post could not be updated. Please fix the errors below.')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    return redirect('home')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        Comment.objects.create(post=post, user=request.user, body=request.POST.get('body'))
        return redirect('post_detail', pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=pk)

def all_posts(request):
    posts = Post.objects.select_related('author').order_by('-created_at')
    return render(request, 'blog/posts.html', {'posts': posts})

def stories_list(request):
    stories = Story.objects.all().order_by('-created_at')
    return render(request, 'blog/stories.html', {'stories': stories})

@login_required
def profile(request):
    """View current user's profile."""
    userprofile = get_object_or_404(UserProfile, user=request.user)
    user_posts = Post.objects.filter(author=request.user).select_related('author').order_by('-created_at')

    return render(request, 'blog/profile.html', {
        'profile_user': request.user,
        'userprofile': userprofile,
        'user_posts': user_posts
    })


@login_required
def user_profile(request, username):
    """View another user's profile and posts."""
    profile_user = get_object_or_404(User, username=username)
    userprofile = get_object_or_404(UserProfile, user=profile_user)
    user_posts = Post.objects.filter(author=profile_user).select_related('author').order_by('-created_at')

    return render(request, 'blog/profile.html', {
        'profile_user': profile_user,
        'userprofile': userprofile,
        'user_posts': user_posts
    })

@login_required
def edit_profile(request):
    """Edit current user's profile"""
    userprofile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    
    return render(request, 'blog/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def create_story(request):
    """Create a new story"""
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            messages.success(request, 'Story created successfully!')
            return redirect('stories')
    else:
        form = StoryForm()
    return render(request, 'blog/create_story.html', {'form': form})

@login_required
def delete_story(request, pk):
    """Delete a story"""
    story = get_object_or_404(Story, pk=pk)
    if story.user != request.user:
        messages.error(request, "You can't delete someone else's story!")
        return redirect('home')
    
    story.delete()
    messages.success(request, "Story deleted successfully.")
    return redirect('stories')

@login_required
def view_story(request, pk):
    """View a story and track the view"""
    story = get_object_or_404(Story, pk=pk)
    
    # Track the view
    if request.user != story.user:
        StoryView.objects.get_or_create(story=story, viewer=request.user)
    
    return render(request, 'blog/view_story.html', {'story': story})

@login_required
def story_viewers(request, pk):
    """View who viewed a story"""
    story = get_object_or_404(Story, pk=pk)
    
    # Only the story owner can see viewers
    if story.user != request.user:
        messages.error(request, "You can only view viewers for your own stories!")
        return redirect('stories')
    
    viewers = story.story_views.all().order_by('-viewed_at')
    return render(request, 'blog/story_viewers.html', {
        'story': story,
        'viewers': viewers
    })
