from django.contrib.auth import authenticate, get_user, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import datetime

from auctions.models import User, Listing, Comment, Watchlist
from auctions.forms import ListingForm, CommentForm

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active__exact=True),
        "title": "Active Listings",
        })

def mylistings(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(owner__exact=get_user(request)),
        "title": "My Listings",
    })


def watchlist(request):
    wtc=Watchlist.objects.filter(user__exact=get_user(request))
    items=[]
    for it in wtc:
        items.append(it.item.id)
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(pk__in=items),
        "title": "My Watchlist",
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            obj=Comment()
            obj.item = Listing.objects.get(pk=listing_id)
            obj.user = get_user(request)
            obj.comment = form.cleaned_data['comment']
            obj.save()
            isWatched = Watchlist.objects.filter(user__exact=get_user(request), item__exact=listing_id)
            starred = (isWatched.count()>0)
            return render(request, "auctions/listing.html", context={
                "listing": Listing.objects.get(pk=listing_id),
                "comments": Comment.objects.filter(item__exact=listing_id).order_by("-timestamp"),
                "form": CommentForm(),
                "starred": starred,
            })
        else:
            isWatched = Watchlist.objects.filter(user__exact=get_user(request), item__exact=listing_id)
            starred = (isWatched.count()>0)
            return render(request, "auctions/listing.html", context={ 
                "listing": Listing.objects.get(id=listing_id),
                "comments": Comment.objects.filter(item__exact=listing_id).order_by("-timestamp"),
                "form": form,
                "starred": starred,
                 })
    else:
        isWatched = Watchlist.objects.filter(user__exact=get_user(request), item__exact=listing_id)
        starred = (isWatched.count()>0)
        return render(request, "auctions/listing.html",{
            "listing": Listing.objects.get(id=listing_id),
            "comments": Comment.objects.filter(item__exact=listing_id).order_by("-timestamp"),
            "form": CommentForm(),
            "starred": starred,
    })

def create(request):
    if (request.method == "POST" ):
        form=ListingForm(request.POST, request.FILES)
        if form.is_valid():
            xReq = Listing()
            xReq.active = form.cleaned_data['active']
            xReq.title = form.cleaned_data['title']
            xReq.picture = form.cleaned_data.get('picture')
            xReq.description = form.cleaned_data['description']
            xReq.initialPrice = form.cleaned_data['initialPrice']
            xReq.currentPrice = form.cleaned_data['currentPrice']
            xReq.creationDate = datetime.datetime.now()
            xReq.category = form.cleaned_data['category']
            xReq.owner = User.objects.get(username=get_user(request))
            xReq.save()
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/create.html", {
            "form": ListingForm,
        })

def watch(request, listing_id):
    usr=get_user(request)
    lst=Listing.objects.get(pk=listing_id)
    wtc=Watchlist.objects.filter(user__exact=usr,item__exact=lst)
    if wtc.count()>0:
        wtc.delete()
    else:
        wtc=Watchlist.objects.create(user=usr, item=lst)
        wtc.save()

    print(listing_id)
    return HttpResponseRedirect(reverse('listing',args=(listing_id,)))

