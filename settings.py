# settings.py

# Import tajných klíčů ze souboru secret.py
from secret import BOT_TOKEN, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET

# Výchozí subreddit a typ řazení 
DEFAULT_SUBREDDIT = "memes"
DEFAULT_SORT = "hot"

# Možné hodnoty řazení
VALID_SORTS = {"hot", "new", "top", "rising", "controversial"}

# Cesta k ffmpeg potřebný pro youtube
FFMPEG_PATH = 'C:/ffmpeg/bin/ffmpeg.exe'

#Keywords pro náhodné přehrávání z youtube
KEYWORDS = [
    "pop music", "rock hits", "top charts",
    "hip hop music", "indie songs", "jazz music", "sad songs", "kabát"
]