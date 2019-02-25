import praw  # Python Reddit API Wrapper
import urllib.request
import json
import time
import logging
from psaw import PushshiftAPI

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

        api = PushshiftAPI(reddit)
        search_time = int(start_time)
        while True:
            gen = api.search_comments(after=search_time, q="pvst")
            first = True

            for comment in gen:
                # Look for keywords in comments
                if "!pvst" in comment.body:
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
                            + "\n\n_____\n\n^(PewDiePie vs T-Series Bot 1.3) ^\[[Feedback/Info](https://www.reddit.com/user/pewdsvstseries_bot/comments/abyg5n/pewdiepie_vs_tseries_bot/)\] ^\[[LiveSubCount](https://www.reddit.com/user/pewdsvstseries_bot/comments/aunvok/pewdiepie_vs_tseries_live_sub_count/)\]"
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
                if first:
                    search_time = int(comment.created_utc)
                    first = False
            time.sleep(2)
    except:
        logging.error("Cannot connect")

    time.sleep(30)
    # Automatic restart after 30 seconds
    logging.info("Restarting...")
