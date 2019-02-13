import praw  # Python Reddit API Wrapper
import urllib.request
import json
import time
import logging

logging.basicConfig(
    filename="pvst.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.info("Bot Started")

g_api = "https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="


def get_sub_count(yt_name):
    data = urllib.request.urlopen(g_api + yt_name + "&key=" + key).read()
    subs = json.loads(data.decode("utf-8"))["items"][0]["statistics"]["subscriberCount"]
    return subs


while True:
    try:
        start_time = time.time()
        key = "ytapikeyhere"

        # Reddit login info
        reddit = praw.Reddit(
            client_id="client101",
            client_secret="itsasecret",
            password="1234",
            user_agent="Pewdiepie vs T-Series Bot",
            username="redditusername",
        )

        logging.info("Logged in as " + str(reddit.user.me()))

        subreddit = reddit.subreddit("PewdiepieSubmissions+pewdiepie")  # subreddits

        for comment in subreddit.stream.comments():
            # Look for keywords in comments
            if "!pewdsvstseries" in comment.body or "!pvst" in comment.body:
                # Makes sure that the bot only replies to new comments
                if comment.created_utc > start_time:
                    logging.info("Processing request")
                    try:
                        subsp = get_sub_count("PewDiePie")
                        subst = get_sub_count("tseries")

                        # Reply to comment
                        comment.reply(
                            "[PewDiePie](https://www.youtube.com/user/pewdiepie): "
                            + "{:,d}".format(int(subsp))
                            + "\n\n[T-Series](https://www.youtube.com/user/tseries): "
                            + "{:,d}".format(int(subst))
                            + "\n\n**Difference**: "
                            + "{:,d}".format(abs(int(subsp) - int(subst)))
                            + "\n\n_____\n\n^(PewDiePie vs T-Series Bot 1.2) ^[Feedback/Info](https://www.reddit.com/user/pewdsvstseries_bot/comments/abyg5n/pewdiepie_vs_tseries_bot/)"
                        )
                        # Log the reply
                        logging.info(
                            "PewDiePie: "
                            + "{:,d}".format(int(subsp))
                            + "  T-Series: "
                            + "{:,d}".format(int(subst))
                            + "  Difference: "
                            + "{:,d}".format(abs(int(subsp) - int(subst)))
                        )
                    except:
                        logging.error("Error while processing")
    except:
        logging.error("Cannot connect")

    time.sleep(30)
    # Automatic restart after 30 seconds
    logging.info("Restarting...")
