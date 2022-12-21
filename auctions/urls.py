from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<str:name>", views.listing, name="listing"),
    path("listing/<str:name>/comment", views.comment, name="comment"),
    path("listing/<str:name>/bid", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<str:name>/close", views.close, name="close"),
    path("watchlist/remove", views.remove, name="remove"),
    path("categories", views.categories, name='categories'),
    path("categories/<str:category>", views.category, name='category')
]