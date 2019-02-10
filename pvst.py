import praw   #Python Reddit API Wrapper
import urllib.request
import json
import time
import logging

logging.basicConfig(filename='pvst.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info("Bot Started")
while True:
    try:
        start_time = time.time()
        key = "ytapikeyhere"

        reddit = praw.Reddit(client_id='client101',
                             client_secret='itsasecret',
                             password='1234',
                             user_agent='Pewdiepie vs T-Series Bot',
                             username='redditusername') #reddit login info

        logging.info("Logged in as " + str(reddit.user.me()))

        subreddit = reddit.subreddit("PewdiepieSubmissions+pewdiepie")  # subreddits



        for comment in subreddit.stream.comments():
            if "!pewdsvstseries" in comment.body or "!pvst" in comment.body:   #look for keywords
                if comment.created_utc > start_time:             #makes sure that the bot only replies to new comments
                    logging.info("Processing request")
                    try:
                        datap = urllib.request.urlopen(
                            "https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=" + "PewDiePie" + "&key=" + key).read() #gets channel info
                        subsp = json.loads(datap.decode('utf-8'))["items"][0]["statistics"]["subscriberCount"] #gets subscriber count

                        datat = urllib.request.urlopen(
                            "https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=" + "tseries" + "&key=" + key).read() #gets channel info
                        subst = json.loads(datat.decode('utf-8'))["items"][0]["statistics"]["subscriberCount"]       #gets subscriber count
                        comment.reply("[PewDiePie](https://www.youtube.com/user/pewdiepie): " + "{:,d}".format(int(subsp)) + "\n\n[T-Series](https://www.youtube.com/user/tseries): " + "{:,d}".format(
                            int(subst)) + "\n\n**Difference**: " + "{:,d}".format(abs(int(subsp) - int(
                            subst))) + "\n\n_____\n\n^(PewDiePie vs T-Series Bot 1.2) ^[Feedback/Info](https://www.reddit.com/user/pewdsvstseries_bot/comments/abyg5n/pewdiepie_vs_tseries_bot/)") #replies
                        logging.info("PewDiePie: " + "{:,d}".format(int(subsp)) + "  T-Series: " + "{:,d}".format(
                            int(subst)) + "  Difference: " + "{:,d}".format(abs(int(subsp) - int(subst))))
                    except:
                        logging.error("Error while processing")
    except:
        logging.error("Cannot connect")

    time.sleep(30)
    logging.info("Restarting...")  # automatic restart after 30 seconds

