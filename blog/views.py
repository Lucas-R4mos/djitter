from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'blog/main.html', context=None)

def entrar(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blog:home'))

    if request.method == 'POST':
        from django.contrib.auth import authenticate, login

        username = request.POST['user']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            return HttpResponseRedirect(reverse('blog:home'))
        else:
            return HttpResponse('<h1>Não deu certo autenticar</h1>')


    return render(request, 'blog/entrar.html', context=None)

def inscrever(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blog:home'))

    if request.method == "POST":
        from django.contrib.auth.models import User
        from django.db import IntegrityError
        from django.contrib.auth import authenticate, login

        username = request.POST['user']
        password = request.POST['password']

        try:
            newUser = User.objects.create_user(username=username, password=password)
            newUser.save()

        except IntegrityError:
            context = {
                'user_error': 'Este nome de usuário já está em uso :/'
            }

            return render(request, 'blog/inscrever.html', context)

        else:
            user = authenticate(username=username, password=password)
            login(request, user)

        return HttpResponseRedirect(reverse('blog:inscrever2'))

    return render(request, 'blog/inscrever.html', context=None)

def inscrever2(request):
    user = request.user

    context = {
        'user': user,
    }

    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']

        user.first_name = firstName
        user.last_name = lastName

        user.save()

        return HttpResponseRedirect(reverse('blog:inscrever3'))

    return render(request, 'blog/inscrever2.html', context)

def inscrever3(request):
    from .models import Profile

    user = request.user

    context = {
        'user': user
    }

    if request.method == 'POST':
        bio = request.POST['bio']

        profile = Profile(user=user, bio=bio)
        profile.save()

        return HttpResponseRedirect(reverse('blog:home'))

    return render(request, 'blog/inscrever3.html', context) 

@login_required(login_url='blog:entrar')
def home(request):
    from .models import Post

    loggedUser = request.user

    posts = Post.objects.order_by('-published_at')

    context = {
        'loggedUser': loggedUser,
        'posts': posts,
    }

    return render(request, 'blog/home.html', context)

def logout_view(request):
    from django.contrib.auth import logout

    logout(request)

    return HttpResponseRedirect(reverse('blog:index'))

@login_required(login_url='blog:entrar')
def novoPost(request):
    from .models import Post

    user = request.user

    postContent = request.POST['content']

    post = Post(author=user, content=postContent)
    post.save()

    return HttpResponseRedirect(reverse('blog:home'))

def perfil(request, username):
    from django.contrib.auth.models import User
    from .models import Profile, Post

    loggedUser = request.user

    user = User.objects.get(username=username)

    profile = Profile.objects.get(user_id=user.id)

    posts = Post.objects.filter(author_id=user.id).order_by('-published_at')

    context = {
        'user': user,
        'profile': profile,
        'posts': posts,
        'loggedUser': loggedUser,
    }

    if loggedUser == user:
        context['profileOwner'] = True

    return render(request, 'blog/perfil.html', context)