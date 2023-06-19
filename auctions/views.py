from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listings, Comment, Bid


def index(request):
    try:
        items = request.user.watchlist.all()
        counter = 0
        for i in items:
            counter += 1
        get_active_listings = Listings.objects.filter(active=True)
        return render(request, "auctions/index.html", {
            "listings": get_active_listings,
            "categorys": Category.objects.all(),
            "counter": counter
        })
    except AttributeError:
        get_active_listings = Listings.objects.filter(active=True)
        return render(request, "auctions/index.html", {
            "listings": get_active_listings,
            "categorys": Category.objects.all()
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

def createListing(request):
    if request.method == "GET":
        currentUser = request.user
        items = currentUser.watchlist.all()
        counter = 0
        for i in items:
            counter += 1
        get_categorys = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "categorys": get_categorys,
            "counter": counter
        })
    else:
        #get the date from the form
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        img = request.POST["img"]
        category = request.POST["category"]
        currentUser = request.user
        categoryData = Category.objects.get(cat=category)
        #create a bid object
        bid = Bid(bid=float(price), user=currentUser)
        bid.save()
        #create neww listing
        listing = Listings(title=title, price=bid, description=description, listing_creator=currentUser, img=img, category=categoryData)
        listing.save()
        return HttpResponseRedirect(reverse("index"))

def viewCategory(request):
    if request.method == "POST":
        category_selected = request.POST["category"]
        category = Category.objects.get(cat=category_selected)
        get_active_listings = Listings.objects.filter(active=True, category=category)
        return render(request, "auctions/index.html", {
            "listings": get_active_listings,
            "categorys": Category.objects.all()
        })

def item(request, id):
    try:
        itemData = Listings.objects.get(pk=id)
        isActive = itemData.active
        comments = Comment.objects.filter(item=itemData)
        is_item_in_watchlist = request.user in itemData.watchlist.all()
        currentUser = request.user
        items = currentUser.watchlist.all()
        isOwner = request.user.username == itemData.listing_creator.username
        counter = 0
        for i in items:
            counter += 1
        return render(request, "auctions/item.html", {
            "itemData": itemData,
            "is_item_in_watchlist": is_item_in_watchlist,
            "counter": counter,
            "comments": comments,
            "isOwner": isOwner,
            "active": isActive
        })
    except AttributeError:
        itemData = Listings.objects.get(pk=id)
        comments = Comment.objects.filter(item=itemData)
        return render(request, "auctions/item.html", {
            "itemData": itemData,
            "comments": comments
        })

def removeWatchlist(request, id):
    itemData = Listings.objects.get(pk=id)
    currentUser = request.user
    itemData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("item",  args=(id, )))

def addWatchlist(request, id):
    itemData = Listings.objects.get(pk=id)
    currentUser = request.user
    itemData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("item",  args=(id, )))

def viewWatchlist(request):
    currentUser = request.user
    items = currentUser.watchlist.all()
    counter = 0
    for i in items:
        counter += 1
    return render(request, "auctions/watchlist.html", {
        "listings": items,
        "counter": counter
    })

def addComment(request, id):
    itemData = Listings.objects.get(pk=id)
    comment = request.POST["comment"]

    newComment = Comment(author=request.user, item=itemData, comment_text=comment)
    newComment.save()

    return HttpResponseRedirect(reverse("item",  args=(id, )))

def addBid(request, id):
    try:
        bid = request.POST["bid"]
        itemData = Listings.objects.get(pk=id)
        itemPrice = itemData.price.bid
        comments = Comment.objects.filter(item=itemData)
        isOwner = request.user.username == itemData.listing_creator.username
        is_item_in_watchlist = request.user in itemData.watchlist.all()
        if float(bid) > itemPrice:
            updateBid = Bid(user=request.user, bid=bid)
            updateBid.save()
            itemData.price = updateBid
            itemData.save()
            return render(request, "auctions/item.html", {
                "itemData": itemData,
                "message": "Bid was updated!",
                "isOwner": isOwner,
                "update":True,
                "is_item_in_watchlist": is_item_in_watchlist,
                "comments": comments
            })
        else:
            return render(request, "auctions/item.html", {
                "itemData": itemData,
                "message": "Bid failed to updated!",
                "update":False,
                "comments": comments,
                "isOwner": isOwner,
            })
    except:
        if bid == "":
            return render(request, "auctions/item.html", {
                "itemData": itemData,
                "message": "Bid must be filled in!",
                "update":False,
                "comments": comments,
                "isOwner": isOwner,
          })

def closeAuction(request, id):
    itemData = Listings.objects.get(pk=id)
    itemData.active = False
    itemData.save()
    counter = 0
    comments = Comment.objects.filter(item=itemData)
    is_item_in_watchlist = request.user in itemData.watchlist.all()
    isOwner = request.user.username == itemData.listing_creator.username
    return render(request, "auctions/item.html", {
            "itemData": itemData,
            "is_item_in_watchlist": is_item_in_watchlist,
            "counter": counter,
            "comments": comments,
            "isOwner": isOwner,
            "update": True,
            "message": "Auction Closed!"
        })