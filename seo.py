import re

BAD_WORDS = ["ass", "porn", "nude", "xxx"]

def clean_keywords(text):
    words = [w.strip() for w in text.split(",") if w.strip()]
    words = [w for w in words if all(bad not in w.lower() for bad in BAD_WORDS)]
    return ", ".join(sorted(set(words)))

def clean_title(title):
    for bad in BAD_WORDS:
        title = re.sub(bad, "", title, flags=re.IGNORECASE)
    return title.strip()
