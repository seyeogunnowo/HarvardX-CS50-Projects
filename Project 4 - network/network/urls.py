from django.urls import path
from . import views

app_name='network'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("user-profile", views.other_user_profile, name="other_user_profile"),
    path('following', views.following, name="following"),
    path('unfollow', views.unfollow, name="unfollow"),
    path("posts", views.posts, name="posts"),
    path("posts/<int:post_id>", views.get_post, name="get_post"),
    path("posts/like/<int:post_id>", views.like, name="like"),
    path("posts/unlike/<int:post_id>", views.unlike, name="unlike")
]
