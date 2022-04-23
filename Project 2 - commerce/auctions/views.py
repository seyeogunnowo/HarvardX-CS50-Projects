from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .models import User

def index(request):
    if request.method=='POST':
        if (request.POST['category'] != 'none'):
            create_listing=Listing(username=request.POST['username'], title=request.POST['title'], description=request.POST['description'], starting_bid=request.POST['starting_bid'], category=request.POST['category'], image_url=request.POST['image_url'])
            create_listing.save()
            listing=Listing.objects.filter(title=request.POST['title'])
            listing_get_id=listing.values_list('id', flat=True)
            listing_gotten_id=''.join(str(x) for x in listing_get_id)
            save_in_categories=Category(title=request.POST['title'], category=request.POST['category'], listing_id=int(listing_gotten_id))
            save_in_categories.save()
        else:
            create_listing=Listing(username=request.POST['username'], title=request.POST['title'], description=request.POST['description'], starting_bid=request.POST['starting_bid'], image_url=request.POST['image_url'])
            create_listing.save()
        return HttpResponseRedirect(reverse('auctions:index'))
    return render(request, "auctions/index.html", {
    'listings':Listing.objects.all()
    })

def watchlist(request):
    if request.method=='POST':
        listing_id=request.POST['listing_id']
        listing=Listing.objects.get(pk=listing_id)
        listing_title=listing.title
        save_to_watchlist=Watchlist(username=request.user.username, title=listing_title, listing_id=int(listing_id))
        save_to_watchlist.save()
        return render (request, 'auctions/watchlist.html', {
        'watchlist':Watchlist.objects.all(),
        'olisting_id':listing_id
        })
    return render (request, 'auctions/watchlist.html', {
    'watchlist':Watchlist.objects.all()
    })

def listing_page(request):
    if request.method=='GET':
        listing_id=request.GET['listing_id']
        watchlist=Watchlist.objects.filter(username=request.user.username)
        return render (request, 'auctions/listing_page.html', {
        'listing':Listing.objects.get(pk=listing_id),
        'watchlist_list':watchlist.values_list('title', flat=True),
        'comments':Comment.objects.filter(listing=request.GET['listing_title'])
        })
    return render (request, 'auctions/listing_page.html')


def category(request):
    return render (request, 'auctions/category.html')


def category_page(request):
    if request.method=='GET':
        items=Listing.objects.filter(category=request.GET['category'])
        return render (request, 'auctions/category_page.html', {
        'items':items,
        'category':request.GET['category']
        })


def wremove(request):
    if request.method=='POST':
        listing_title=request.POST['listing_title']
        item=Watchlist.objects.filter(title=listing_title)
        item.delete()
        return HttpResponseRedirect(reverse('auctions:watchlist'))

def watchlist_listing(request):
    if request.method=='GET':
        listing_id=request.GET['listing_id']
        return render (request, 'auctions/listing_page.html', {
        'listing':Listing.objects.get(pk=listing_id)
        })
    return render (request, 'auctions/watchlist_listing.html')

def create_listing(request):
    if request.user.is_authenticated:
        return render (request, 'auctions/create_listing.html')
    else:
        return HttpResponse ('You need to login to create listings. Please go back and log in.')

def bids(request):
    if request.method=='POST':
        return render (request, 'auctions/bids.html', {
        'listing_title':request.POST['listing_title'],
        'listing_starting_bid':request.POST['listing_starting_bid'],
        })
    else:
        HttpResponse('Bad request.')

def ldelete(request):
    if request.method=='POST':
        if (request.POST['listing_title'] in Bid.objects.values_list('title', flat=True)):
            l_bid=Bid.objects.filter(title=request.POST['listing_title'])
            all_bids=l_bid.values_list('bid', flat=True)
            highest_bid=max(all_bids)
            winner_queryset=Bid.objects.filter(bid=highest_bid)
            winner_list=winner_queryset.values_list('username', flat=True)
            winner=''.join(str(x) for x in winner_list)
            deactivate=Inactive_Listng(username=request.POST['username'], title=request.POST['listing_title'], description=request.POST['description'], starting_bid=request.POST['starting_bid'], winning_bid=highest_bid, winning_user=winner)
            deactivate.save()
            listing=Listing.objects.filter(title=request.POST['listing_title'])
            listing.delete()
            return render (request, 'auctions/close.html', {
            'winner':winner,
            'bid':highest_bid
            })
        else:
            deactivate=Inactive_Listng(username=request.POST['username'], title=request.POST['listing_title'], description=request.POST['description'], starting_bid=request.POST['starting_bid'])
            deactivate.save()
            listing=Listing.objects.filter(title=request.POST['listing_title'])
            listing.delete()
            watchlist=Watchlist.objects.filter(title=request.POST['listing_title'])
            if (request.POST['listing_title'] in watchlist.values_list('title', flat=True)):
                watchlist.delete()
            return HttpResponseRedirect(reverse('auctions:index'))
    else:
        HttpResponse('Bad request.')

def inactive(request):
    return render (request, 'auctions/inactive.html', {
    'inactive':Inactive_Listng.objects.all()
    })

def inactive_page(request):
    if request.method=='GET':
        listing_id=request.GET['inactive_id']
        return render (request, 'auctions/inactive_page.html', {
        'inactive':Inactive_Listng.objects.get(pk=listing_id),
        })
    return render (request, 'auctions/inactive_page.html')

def comment(request):
    if request.method=='GET':
        return render(request, 'auctions/comment.html', {
        'listing_title':request.GET['listing_title'],
        'listing_id':request.GET['listing_id'],
        })

def comment_conf(request):
    if request.method=='POST':
        comment_save=Comment(username=request.POST['username'], listing=request.POST['l_title'], message=request.POST['message'])
        comment_save.save()
        return render(request, 'auctions/comment_conf.html', {
        'listing_id':request.POST['listing_id'],
        'l_title':request.POST['l_title'],
        'comment':Comment.objects.filter(username=request.POST['username'], listing=request.POST['l_title'])
        })


def placed_bids(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            title_match=Bid.objects.filter(title=request.POST['listing_title'])
            all_bids=(title_match.values_list('bid', flat=True))
            all_titles=Bid.objects.values_list('title', flat=True)
            if ((int(request.POST['listing_starting_bid'])) > (int(request.POST['bid_amount']))):
                return HttpResponse('Cannot place bid. Your bid must be greater or equal to the starting bid. Please go back.')
            else:
                if ((request.POST['listing_title']) in all_titles):
                    for i in all_bids:
                        top_bid=max(all_bids)
                        if ((int(request.POST['bid_amount']) < top_bid) and (int(request.POST['bid_amount']) != top_bid)):
                            return HttpResponse(f'Someone has already bid this or higher than this. Highest bid for this item is currently: {top_bid}')
                        else:
                            save_bids=Bid(username=request.user.username, title=request.POST['listing_title'], starting_bid=request.POST['listing_starting_bid'], bid=request.POST['bid_amount'])
                            save_bids.save()
                            return render (request, 'auctions/placed_bids.html', {
                            'bids':Bid.objects.filter(username=request.user.username)
                            })
                else:
                    save_bids=Bid(username=request.user.username, title=request.POST['listing_title'], starting_bid=request.POST['listing_starting_bid'], bid=request.POST['bid_amount'])
                    save_bids.save()
                    return render (request, 'auctions/placed_bids.html', {
                    'bids':Bid.objects.filter(username=request.user.username)
                    })
        else:

            return render (request, 'auctions/placed_bids.html', {
            'bids':Bid.objects.filter(username=request.user.username)
        })
    else:
        return HttpResponse('You are not logged in.')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
