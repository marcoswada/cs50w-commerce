from django.contrib.auth import authenticate, get_user, login, logout
from django.db import IntegrityError
from django.db.utils import Error
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import datetime

from auctions.models import User, Listing, Comment, Bid, Category
from auctions.forms import ListingForm, CommentForm, BidForm

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active__exact=True),
        "title": "Active Listings",
        })

def mylistings(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(owner__exact=get_user(request)).filter(active__exact=True),
        "title": "My Listings",
    })


def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(watchedBy__in=[User.objects.get(username__exact=get_user(request)),]).filter(active__exact=True),
        "title": "My Watchlist",
    })

def category(request, category_id):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category__exact=category_id).filter(active__exact=True),
        "title": "Items on " + Category.objects.get(pk=category_id).description + " category"
    })

def finished(request):
    return render(request,"auctions/index.html",{
        "listings": Listing.objects.filter().filter(active__exact=False),
        "title": "Finished auctions"
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

def listing(request, listing_id, ):
    usr=User.objects.get(username__exact=get_user(request))
    starred=usr in Listing.objects.get(pk=listing_id).watchedBy.all()
    isowner = (get_user(request)==Listing.objects.get(pk=listing_id).owner)
    message=request.GET.get('message', None)
    if Listing.objects.get(pk=listing_id).bid_set.count()==0:
        winning_bidder=False
    else:
        winning_bidder=Listing.objects.get(pk=listing_id).bid_set.order_by("-value")[0].bidder==get_user(request)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            obj=Comment()
            obj.item = Listing.objects.get(pk=listing_id)
            obj.user = get_user(request)
            obj.comment = form.cleaned_data['comment']
            obj.save()
            return HttpResponseRedirect(reverse('listing',args=(listing_id,))+"#commentsform")
        else:
            return render(request, "auctions/listing.html", context={ 
                "listing": Listing.objects.get(id=listing_id),
                "comments": Comment.objects.filter(item__exact=listing_id).order_by("-timestamp"),
                "form": form,
                "starred": starred,
                "isowner": isowner,
                "bidform": BidForm(listing_id),
                "bids": Bid.objects.filter(item=listing_id).order_by("-bidDate"),
                "message": message,
                "winning_bidder": winning_bidder,
                 })
    else:
        return render(request, "auctions/listing.html",{
            "listing": Listing.objects.get(id=listing_id),
            "comments": Comment.objects.filter(item__exact=listing_id).order_by("-timestamp"),
            "form": CommentForm,
            "starred": starred,
            "isowner": isowner,
            "bidform": BidForm(listing_id),
            "bids": Bid.objects.filter(item=listing_id).order_by("-bidDate"),
            "message": message,
            "winning_bidder": winning_bidder,
    })

def create(request):
    if (request.method == "POST" ):
        form=ListingForm(request.POST, request.FILES)
        if form.is_valid():
            xReq = Listing()
            xReq.active = True
            xReq.title = form.cleaned_data['title']
            xReq.picture = form.cleaned_data.get('picture')
            xReq.description = form.cleaned_data['description']
            xReq.initialPrice = form.cleaned_data['initialPrice']
            xReq.currentPrice = xReq.initialPrice
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
    usr=User.objects.get(username__exact=get_user(request))
    lst=Listing.objects.get(pk=listing_id)
    if usr in lst.watchedBy.all():
        lst.watchedBy.remove(usr)
    else:
        lst.watchedBy.add(usr)
    return HttpResponseRedirect(reverse('listing',args=(listing_id,)))

def finish(request, listing_id):
    if request.method=='GET':
        lst=get_object_or_404(Listing, pk=listing_id)
        if get_user(request)==lst.owner:
            lst.active=False
            lst.save()
            return HttpResponseRedirect(reverse('listing',args=(listing_id,)))
        else:
            message="You can't finish someone else's auction"
            return HttpResponseRedirect(reverse('listing',args=(listing_id,))+'?message='+message)

    #return HttpResponse("not implemented yet")

def bid(request, listing_id):
    if request.method=='POST':
        form=BidForm(listing_id, request.POST)
        if form.is_valid():
            x=Bid()
            x.bidDate=datetime.datetime.now()
            x.bidder=User.objects.get(username__exact=get_user(request))
            x.item=Listing.objects.get(pk=listing_id)
            x.value=form.cleaned_data['value']
            x.save()
            lst=Listing.objects.get(pk=listing_id)
            lst.currentPrice=form.cleaned_data['value']
            lst.save()
            return HttpResponseRedirect(reverse('listing',args=(listing_id,))+"#bidsform")
        else:
            message="Your bid is lower than the current price"
            return HttpResponseRedirect(reverse('listing', args=(listing_id,))+'?message='+message+"#bidsform")

def categories(request):
    categories = Category.objects.all()
    return render(request,"auctions/categories.html", {"categories": categories})

