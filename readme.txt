Module Required:
    Tweepy

Note: Developer account is required to make this bot work.

Create a file config.py and write the following data in that:
# Start
    CONSUMER_KEY = "your consumer key"
    CONSUMER_SECRET_KEY = "your consumer secret key"
    ACCESS_TOKEN = "your access token"
    ACCESS_TOKEN_SECRET = "your access token secret"
# End

** You will get all the above specified values after applying for the developer account.

In tbot.py file you can the change the phrase and responce according to your liking.
If the phrase is present in the mention tweet the responce text will be posted in reply to that tweet else the mention tweet will be retweeted.
All the mention tweets will be liked.

When we repeatedly try to fetch information tweepy.RateLimitError occurs after which we are not able to fetch information for next 15 minutes hence, when any error occurs, the bot goes to sleep for 15 minutes. 