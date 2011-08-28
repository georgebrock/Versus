Versus
======

Rank the places you visit and get recommendations of new places based on other Foursquare users with similar tastes.

The recommendations algorithms are based on the first few chapters of [Programming Collevtive Intelligence by Toby Segaran](http://shop.oreilly.com/product/9780596529321.do)

This is a quick, experimental project mostly built in one day. It won't scale well to lots of users.

To run the app:

1. Change the `PROJECT_URL` setting so that it points to your running instance.
2. [Get a Foursquare consumer key](https://foursquare.com/oauth/) and set the consumer's callback URL to be `http://your-url-here/authenticated`.
3. Set the `VERSUS_FOURSQUARE_CLIENT_ID` and `VERSUS_FOURSQUARE_SECRET` environment variables.
4. Install the requirements using `pip install -r requirements.txt` (you probably want to do this inside a [virtualenv](http://pypi.python.org/pypi/virtualenv).
5. Run the server with `versus/manage.py runserver`
