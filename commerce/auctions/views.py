from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse

from .models import User,Listing,Watchlist,Bids,Comments

def index(request):
    listings = Listing.objects.filter(is_active=True)
    congratmessage = None

    if request.user.is_authenticated:
        user = request.user
        won_listings = []
        inactive_listings = Listing.objects.filter(creator=user, is_active=False)
      
        for listing in inactive_listings:
            current_bid = listing.current_bid
            winner = Bids.objects.filter(listing=listing, owner=user, bidprice=current_bid)
            if winner.exists():
                won_listings.append(listing.title)

        if won_listings:
            congratmessage = "Congratulations! You have won the following auctions: " + ", ".join(won_listings)

    return render(request, "auctions/index.html", {
        "listing": listings,
        "congratmessage": congratmessage
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

def makelisting(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST.get("category", "")
        user = request.user

        if not title or not price or not description:
            return render(request, "auctions/makelisting.html", {
                "error": "Every Field except image and category are required"
            })


        elif Listing.objects.filter(title=title).exists():
            return render(request, "auctions/makelisting.html", {
                "error": "Title already exists"
            })
        else:
            listing = Listing(
                title=title,
                description=description,
                image=imageurl,
                category=category,
                creator=user,
                price=price
            )
            listing.save()

        listtd = Listing.objects.filter(is_active=True)
        return render(request, "auctions/index.html", {
            "listing": listtd,
            "congratmessage": f"Congratulations! Listing  has been created successfully."
        })

    return render(request, "auctions/makelisting.html")

def listingdetails(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    watchlist = Watchlist.objects.filter(listing=listing, user=user)
    if watchlist.exists():
        message = "Remove from watchlist"
    else:
        message = "Add to watchlist"

    error = None
    if request.method == "POST":
        if "bid_amount" in request.POST:
            bid_amount = int(request.POST["bid_amount"])
            highest_bid = listing.bids.order_by('-bidprice').first()

            if bid_amount >= listing.price and (not highest_bid or bid_amount > highest_bid.bidprice):
                bid = Bids(owner=user, bidprice=bid_amount, listing=listing)
                bid.save()
                listing.current_bid = bid_amount
                listing.save()
            else:
                error = "Bid must be at least as large as the starting bid and greater than any other bids."
        elif "comment" in request.POST:
            comment_text = request.POST["comment"]
            comment = Comments(commentdescription=comment_text, maker=user, listing=listing)
            comment.save()
        elif "close_auction" in request.POST and user == listing.creator:
            listing.is_active = False
            listing.save()

    comments = listing.comments.all()

    return render(request, "auctions/listingdetails.html", {
        "listing": listing,
        "message": message,
        "error": error,
        "comments": comments
    })

def add_to_watchlist(request):
    if request.method == "POST":
        listingid = request.POST["listing_id"]
        listing = Listing.objects.get(id=listingid)
        user = request.user
        watchlist = Watchlist(user=user, listing=listing)
        watchlist.save()
        return redirect('listingdetails', listing_id=listingid)
    return redirect('index')
def remove_from_watchlist(request):
    if request.method == "POST":
        listingid = request.POST["listing_id"]
        listing = Listing.objects.get(id=listingid)
        user = request.user
        watchlist = Watchlist.objects.filter(user=user, listing=listing)
        watchlist.delete()
        return redirect('listingdetails', listing_id=listingid)
    return redirect('index')
def watchlist(request):
    user=request.user
    watchlist=Watchlist.objects.filter(user=user)
    listings=[item.listing for item in watchlist]
    listing=[item for item in listings if item.is_active]
    return render(request, "auctions/watchlist.html",{
        "listing":listing
    })

def category(request):
    if request.method == "POST":
        category=request.POST["category"]
        listingc = Listing.objects.filter(category=category, is_active=True)
        return render (request,"auctions/category.html",{
            "listing":listingc
        })

    return render(request,"auctions/category.html",{
        "messagec":"Select a category to display the listings in that category"
    })
