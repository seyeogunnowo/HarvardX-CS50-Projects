from django.urls import path

from . import views

app_name='auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create-listing', views.create_listing, name='create_listing'),
    path('listing', views.listing_page, name='listing_page'),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist-listing", views.watchlist_listing, name="watchlist_listing"),
    path("bids", views.bids, name="bids"),
    path("placed-bids", views.placed_bids, name="placed_bids"),
    path("ldelete", views.ldelete, name="ldelete"),
    path("wremove", views.wremove, name="wremove"),
    path("comment", views.comment, name="comment"),
    path("comment-conf", views.comment_conf, name="comment_conf"),
    path("inactive-listings", views.inactive, name="inactive"),
    path("inactive-page", views.inactive_page, name="inactive_page"),
    path("category", views.category, name="category"),
    path("category-page", views.category_page, name="category_page")
]
