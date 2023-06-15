from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, Postform
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.

#home
def home(request):
    posts = Post.objects.all()
    user = request.user
    context = {"post":posts,}
    return render(request, 'base/home.html', context)

#about
def about(request):
    return render(request, 'base/about.html')

#contact
def contact(request):
    return render(request, 'base/contact.html')

#dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        fullName = user.get_full_name()
        gps = user.groups.all()
        context = {'posts':posts, 'fullName':fullName, 'groups':gps}
        return render(request, 'base/dashboard.html', context)
    else:
        return redirect('login')
#login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = LoginForm(request=request, data= request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            passw = form.cleaned_data['password']
            user = authenticate(username=uname, password=passw)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect('dashboard')
            else:
                messages.error(request, "Username or Password is incorrect")
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'base/login.html', context)
#signup
def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations you have been registered as Blogger on Our Website")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            return redirect('dashboard')
    else:
        form = SignupForm()

    context = {'form':form}
    return render(request, 'base/signup.html', context)
#logout
def user_logout(request):
    logout(request)
    return redirect('/')

#Add New Post
@login_required(login_url='login')
def add_post(request):
    name = request.user
    form = Postform()
    print(name)
    if request.method == "POST":
        form = Postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.name = name
            post.save()
            return redirect('dashboard')
    else:
        form = Postform()
    context = {'form':form, 'name':name}
    return render(request, 'base/addpost.html', context)
    
#Update New Post
@login_required(login_url='login')
def update_post(request, id):
    if request.method == 'POST':
        po = Post.objects.get(pk=id)
        form = Postform(request.POST, instance=po)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        po = Post.objects.get(pk=id)
        form = Postform(instance=po)
    context = {'form':form}
    return render(request, 'base/updatepost.html', context)
    
#Update New Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            po = Post.objects.get(pk=id)
            po.delete()
        return redirect('dashboard')
    
