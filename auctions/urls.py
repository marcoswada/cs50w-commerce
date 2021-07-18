from django.urls import path, re_path
#from django.conf.urls import url
from django.conf.urls.static import static

#from commerce.settings import MEDIA_ROOT
from commerce import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("create", views.create, name="create"),
    path("watch/<int:listing_id>", views.watch, name="watch"),
    path("mylistings", views.mylistings, name="mylistings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("finish/<int:listing_id>", views.finish, name="finish"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("finished", views.fini)
]
