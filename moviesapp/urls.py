from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('details/<int:id>/', DetailView.as_view(), name='detail'),
    path('details/movie/<int:movie_id>/like/', LikeMovieView.as_view(), name='like_movie'),
    path('details/movie/<int:movie_id>/comment/', CommentView.as_view(), name='comment_movie'),
    path('details/comment/<int:comment_id>/like/', LikeCommentView.as_view(), name='like_comment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
