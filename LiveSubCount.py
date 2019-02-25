import praw  # Python Reddit API Wrapper
import urllib.request
import json
import time
import logging

logging.basicConfig(
    filename="pvstlive.log",
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

        key = "---"

        # Reddit login info
        reddit = praw.Reddit(
            client_id='---',
            client_secret='---',
            password='---',
            user_agent='Pewdiepie vs T-Series Bot',
            username='---',
        )

        submission = reddit.submission(id='---')

        logging.info("Logged in as " + str(reddit.user.me()))

        while True:

            subsp = get_sub_count("PewDiePie")
            subst = get_sub_count("tseries")

            # Edit Submissions
            submission.edit(
                    "[PewDiePie](https://www.youtube.com/user/pewdiepie): "
                    + "{:,d}".format(int(subsp))
                    + "\n\n[T-Series](https://www.youtube.com/user/tseries): "
                    + "{:,d}".format(int(subst))
                    + "\n\n**Difference**: "
                    + "{:,d}".format(abs(int(subsp) - int(subst)))
                    + "\n\n_____\n\n^(PewDiePie vs T-Series Bot 1.3) ^[Feedback/Info](https://www.reddit.com/user/pewdsvstseries_bot/comments/abyg5n/pewdiepie_vs_tseries_bot/)"
            )


            time.sleep(10)

    except:
        logging.error("Cannot connect")

    time.sleep(30)
    # Automatic restart after 30 seconds
    logging.info("Restarting...")
