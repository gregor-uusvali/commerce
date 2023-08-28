# Commerce

Ebay like website made with django. CS50 course project.
Languages: Pyhton, Javascript

## Features

- Add items to shop
- Users can bid on items
- Users get notified when they have won the bidding
- Comments on listings

# Specification

This project is a simple auction website where users can buy and sell items:

- Models: application has three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings.
- Create Listing: Users can visit a page to create a new listing. They can specify a title for the listing, a text-based description, and what the starting bid should be. Users can provide a URL for an image for the listing and/or a category.
- Active Listings Page: The default route of your web application lets users view all of the currently active auction listings.
- Listing Page: Clicking on a listing takes the users to a page specific to that listing. On that page, users can view all details about the listing, including the current price for the listing.

* If the user is signed in, the user can add the item to their “Watchlist.” If the item is already on the watchlist, the user can remove it.
* If the user is signed in, the user can bid on the item.
* If the user is signed in and is the one who created the listing, the user can close the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
* Users who are signed in can add comments to the listing page.

- Watchlist: Users who are signed in can visit a Watchlist page, which should display all of the listings that a user has added to their watchlist.
- Categories: Users can visit a page that displays a list of all listing categories.

## Instructions

Run app from the command line. You must have all the dependencies installed (sqlite 3 etc).

```
$ ./run.sh
```
[Demo](http://176.112.158.18:8090/)
### Forum users for testing

Testuser `ork1:ork123` <br/>

### Dependencies

- Sqlite3 - Database
- Bcrypt - Password encryption
- UUID - Cookie authenitication
- Django

## Author

[Gregor Uusväli](https://github.com/gregor-uusvali/)
