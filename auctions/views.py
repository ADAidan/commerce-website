from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings':listings
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

def create_listing(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        image = request.POST['image']
        category = request.POST['category']
        id = request.POST['id']
        user_id = User.objects.get(pk=id)
        l = Listing(name = title, description = description, 
                    price = price, date_created = datetime.datetime.now(), 
                    category = category, image = image, user = user_id)
        l.save()

        return HttpResponseRedirect(reverse('index'))
    
    else:
        return render(request, "auctions/create.html")

def listing(request, name):
    listing = Listing.objects.get(name=name)
    try:
        bids = Bid.objects.filter(listing=listing.id)
        highest_bid = 0
        bidder = None
        for bid in bids:
            if bid.price > highest_bid:
                highest_bid = bid.price
                bidder = str(bid.user)
    except:
        highest_bid = None
        bidder = None

    try:
        comments = Comment.objects.filter(listing=listing.id)
    except:
        comments = None
    
    try:
        watchlist = Watchlist.objects.get(user=request.user)
        watchlist = watchlist.listings.get(name=name)
        watchlist = True
    except:
        watchlist = None

    return render(request, "auctions/listing.html", {
        'listing':listing,
        'bid':highest_bid,
        'bidder':bidder,
        'comments':comments,
        'watchlist':watchlist
    })

@login_required
def bid(request, name):
    if request.method == 'POST':
        try:
            new_bid = float(request.POST['bid'])
        except:
            return HttpResponse("Not a valid number")
        id = request.POST['id']
        user = User.objects.get(pk=id)
        listing = Listing.objects.get(name=name)
        try:
            bids = Bid.objects.filter(listing=listing.id)
            highest_bid = 0
            for bid in bids:
                if bid.price > highest_bid:
                    highest_bid = bid.price
        except:
            highest_bid = 0

        if new_bid <= listing.price or new_bid <= highest_bid:
            return HttpResponse("bid is too small")
        
        else:
            b = Bid(listing=listing, user=user, price=new_bid)
            b.save()
            listing.price=new_bid
            listing.save()

        try:
            comments = Comment.objects.filter(listing=listing.id)
        except:
            comments = None
        
        return HttpResponseRedirect(reverse('listing', args=[name]))

@login_required
def watchlist(request):
    if request.method == 'POST':
        id = request.POST['user']
        listing = request.POST['listing']
        user = User.objects.get(pk=id)
        try:
            watchlist = Watchlist.objects.get(user=user)
        except:
            w = Watchlist(user=user)
            w.save()
        
        watchlist = Watchlist.objects.get(user=user)
        watchlist.listings.add(listing)
        watchlist.save()
        return render(request, "auctions/watchlist.html", {
            'watchlist':watchlist
        })

    else:
        try:
            watchlist = Watchlist.objects.get(user=request.user.id)
        except:
            watchlist = None

        return render(request, "auctions/watchlist.html", {
            'watchlist':watchlist
        })

@login_required
def comment(request, name):
    listing = Listing.objects.get(name=name)
    comment = request.POST['comment']
    user = request.user
    date = datetime.datetime.now()
    c = Comment(listing=listing, user=user, comment=comment, date=date)
    c.save()
    return HttpResponseRedirect(reverse('listing', args=[listing.name]))

@login_required
def close(request, name):
    listing = Listing.objects.get(name=name)
    listing.closed = True
    listing.save()
    return HttpResponseRedirect(reverse('listing', args=[listing.name]))

@login_required
def remove(request):
    if request.method == 'POST':
        id = request.POST['user']
        listing = request.POST['listing']
        user = User.objects.get(pk=id)
        watchlist = Watchlist.objects.get(user=user)
        watchlist.listings.remove(listing)
        watchlist.save()
        return render(request, "auctions/watchlist.html", {
            'watchlist':watchlist
        })
    
    else:
        return render(request, "auctions/watchlist.html")

def categories(request):
    listings = Listing.objects.all()
    categories = []
    for listing in listings:
        if listing.category not in categories:
            categories.append(listing.category)
        
    
    return render(request, "auctions/categories.html", {
        'categories':sorted(categories)
    })

def category(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/categories.html", {
        'category':category,
        'listings':listings
    })
    