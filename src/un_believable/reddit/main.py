import praw
import json
# from ..utils.logger import init as logger

# logger = logger()

def generate_post(phrase_counts: dict, episode_name: str, episode_link: str) -> str:
    phrases = [f'"{phrase}" said {count} times' for phrase, count in phrase_counts.items() if count > 0]
    title = f"Un-believable Tony bot breakdown for episode {episode_name}"
    if not phrases:
        return "Tony must've been on his best behavior this episode... suspicious. 🤔"

    comment = [
        "🔥 Kill Tony Un-believable Bot is in the house! 🔥",
        f"Here's a Tony-isms breakdown for [{episode_name}]({episode_link})",
        "",
        "\n".join(f"* ✅ {p}" for p in phrases),
        "",
        "If Tony says it, I count it. If I miss one, you're too sober. 🍻",
        "🙌 Feel free to contribute to me: https://github.com/simecipol/un_believable 🤗"
    ]

    return title, "\n\n".join(comment)
def post(phrase_counts: dict, episode_name: str, episode_link: str):
    with open("reddit.json", "r") as file:
        config = json.load(file)

    reddit = praw.Reddit(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        user_agent=config["user_agent"],
        username=config["username"],
        password=config["password"]
    )

    subreddit = reddit.subreddit("Killtony") 
# body = """Hey degenerates,

# 🤡 Ever wondered just how many times Tony Hinchcliffe says “Un-believable!” or "Ohh my gooood" or any other nonsense phrase in an episode? Probably not. But I did, so I built a bot to track it for you.

# Starting with tomorrow's episode, UnbelievableTonyBot will be counting every single stupid phrase from Tony and posting the stats. If Tony goes on a streak, you'll know. If he holds back, well… that's un-believable.

# What to expect? Here is a backtestng example:

# [#711 - ANDREW SCHULZ, DERIC POSTON](https://www.youtube.com/watch?v=z-21SI0mtv4)

# 🔥 Kill Tony Un-believable Bot is in the house! 🔥
# Here's a Tony-isms breakdown for this episode:

# ✅ "unbelievable" said 10 times\n
# ✅ "oh shit" said 1 times\n
# ✅ "absolutely incredible" said 3 times\n
# ✅ "holy shit" said 5 times\n
# ✅ "what the fuck" said 5 times\n
# ✅ "wow" said 20 times\n
# ✅ "jesus christ" said 1 times\n
# ✅ "incredible" said 13 times\n
# ✅ "oh my god" said 6 times\n

# If Tony says it, I count it. If I miss one, you're too sober. 🍻

# 💡 Want to contribute? Check out the stats in a few episodes for the repo link.

# Stay tuned for the first stats drop tomorrow. Let's see just how un-believable this gets."""

# subreddit.submit("Introducing UnbelievableTonyBot - Tracking Tony's Favorite Phrases!", selftext=body)

    title, body = generate_post(phrase_counts, episode_name, episode_link)
    subreddit.submit(title=title, selftext=body)