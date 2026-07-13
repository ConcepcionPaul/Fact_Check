import re
from pathlib import Path
from config import STOPWORDS_FILE
STOPWORDS = set()

def load_stopwords():
    sw = set()
    p = Path(STOPWORDS_FILE)
    if p.exists():
        with p.open('r', encoding='utf-8') as f:
            for line in f:
                w = line.strip()
                if not w: continue
                sw.add(w.lower())
    return sw

def reload_stopwords():
    global STOPWORDS
    STOPWORDS = load_stopwords()
    return STOPWORDS

# initialize
STOPWORDS = load_stopwords()

def clean_text(text):
    if text is None: return ''
    s = str(text).lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def tokenize(text):
    t = clean_text(text)
    if not t: return []
    toks = t.split()
    toks = [w for w in toks if w not in STOPWORDS]
    return toks
