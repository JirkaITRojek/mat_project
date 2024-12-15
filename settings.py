# settings.py

# Import tajných klíčů ze souboru secret.py
from secret import BOT_TOKEN, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET

# Výchozí subreddit a typ řazení
DEFAULT_SUBREDDIT = "memes"
DEFAULT_SORT = "hot"

# Možné hodnoty řazení
VALID_SORTS = {"hot", "new", "top", "rising", "controversial"}
