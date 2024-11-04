from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy, reverse
from .models import *
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.utils import timezone


class RegisterView(View):
    def get(self, request):
        return render(request, 'moviesapp/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        print(user)
        messages.success(request, "Registration successful. You can now log in.")
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'moviesapp/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('index'))
            else:
                messages.error(request, "Invalid email or password")
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('index')


class IndexView(TemplateView):
    template_name = 'moviesapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = timezone.now().date()

        context['latest_movies'] = Movie.objects.filter(
            release_date__isnull=True
        ).order_by('-created_at')[:10]

        context['upcoming_movies'] = Movie.objects.filter(
            release_date__gt=current_date
        ).order_by('release_date')[:4]

        return context


class DetailView(TemplateView):
    template_name = 'moviesapp/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_id = self.kwargs.get('id')
        movie = get_object_or_404(Movie, id=movie_id)

        context['movie'] = movie
        context['videos'] = movie.videos.all()
        context['screenshots'] = movie.screenshots.all()
        context['comments'] = movie.comments.all()
        context['tech_specs'] = movie.tech_specs.all()
        context['movie_info'] = movie.movie_info.first()

        movie_category = movie.movie_category
        context['similar_movies'] = Movie.objects.filter(movie_category=movie_category).exclude(id=movie.id)[:3]

        context['total_likes'] = Like.objects.filter(movie=movie).count()

        if self.request.user.is_authenticated:
            context['has_liked'] = Like.objects.filter(movie=movie, user=self.request.user).exists()
        else:
            context['has_liked'] = False

        context['videos'] = movie.videos.all()
        movie_info = movie.movie_info.first()
        if movie_info:
            context['top_cast_names'] = movie_info.top_cast_names.split('\n')
        else:
            context['top_cast_names'] = []

        return context


class LikeMovieView(View):
    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        Like.objects.get_or_create(user=request.user, movie=movie)
        return HttpResponseRedirect(reverse('detail', args=[movie_id]))


class CommentView(View):
    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        content = request.POST.get('comment_text')

        if request.user.is_authenticated:
            user_name = request.user.username
            content['user_name'] = user_name
        else:
            user_name = "Anonymous"

        if content:
            Comment.objects.create(movie=movie, user_name=user_name, comment_text=content)
        return redirect('detail', id=movie_id)

class LikeCommentView(View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        CommentLike.objects.get_or_create(user=request.user, comment=comment)
        return redirect('detail', id=comment.movie.id)