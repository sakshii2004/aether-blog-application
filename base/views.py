from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import CustomUserCreationForm
from .forms import CustomUserCreationForm, BlogForm
from .models import Blog

@login_required(login_url='/login')
def home(request):
    return render(request, 'base/home.html')

def registerUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'base/register.html', context)

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
    context = {'page': page}
    return render(request, 'base/login.html', context)

@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def createBlog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            blog.process_image()
            blog.save()
            return redirect('home')
    else:
        form = BlogForm()
        context = {'form': form}
    return render(request, 'base/create_blog.html', context)

@login_required(login_url='/login')
def readBlog(request, blogID):
    blog = get_object_or_404(Blog, id=blogID)
    comments = Comment.objects.filter(blog = blogID)
    comment_form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return redirect('read-blog', blog.id)
    context = {'blog': blog, 'comments':comments, 'commentform': comment_form}
    return render(request, 'base/read_blog.html', context)

@login_required(login_url='/login')
def likeBlog(request, blogID):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, id=blogID)

        if request.user in blog.liked_by.all():
            blog.liked_by.remove(request.user)
            blog.number_of_likes -= 1
        else:
            blog.liked_by.add(request.user)
            blog.number_of_likes += 1

        blog.save()
        return JsonResponse({'likes': blog.number_of_likes})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def viewProfile(request, userID):
    user = get_object_or_404(User, pk=userID)
    is_owner = user == request.user
    blogs = Blog.objects.filter(author = userID).order_by('-created_on')
    context = {'user_profile': user, 'is_owner': is_owner, 'blogs':blogs}
    return render(request, 'base/view_profile.html', context)

@login_required
def editProfile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('view-profile', userID=request.user.id)
    else:
        form = ProfileEditForm(instance=request.user)
    context = {'form': form}
    return render(request, 'base/edit_profile.html', context)

