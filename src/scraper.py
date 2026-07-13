import os, csv, time, random, json, re
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from config import SCRAPED_DIR, SCRAPED_LOG, DATA_DIR
from cleaner import clean_html_text

RULES_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'scraping_rules.json')

def load_rules():
    try:
        with open(RULES_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def fetch_html(url, timeout=15):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36'}
    req = Request(url, headers=headers)
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()

def parse_with_rules(soup, rules):
    title = ''
    content = ''
    date = ''
    subject = rules.get('subject','')
    tsel = rules.get('title')
    if tsel:
        el = soup.select_one(tsel)
        if el: title = el.get_text(' ', strip=True)
    csel = rules.get('text')
    if csel:
        parts = soup.select(csel)
        paragraphs = [p.get_text(' ', strip=True) for p in parts]
        content = '\n'.join(paragraphs)
    dsel = rules.get('date')
    if dsel:
        el = soup.select_one(dsel)
        if el:
            date = el.get('datetime') or el.get_text(' ', strip=True)
    return title, content, subject, date

def fallback_parse(soup):
    title = soup.title.string.strip() if soup.title else ''
    parts = soup.find_all('p')
    paragraphs = [p.get_text(' ', strip=True) for p in parts]
    paragraphs = [p for p in paragraphs if len(p)>40]
    content = '\n'.join(paragraphs)
    return title, content, '', ''

def save_article_csv(target, title, text, subject, date):
    path = os.path.join(DATA_DIR, target)
    new = not os.path.exists(path)
    with open(path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if new:
            writer.writerow(['title','text','subject','date'])
        writer.writerow([title, text, subject, date])

def log_scrape(url, title, subject, date, target, mode, cleaning_status, error=None):
    p = SCRAPED_LOG
    new = not os.path.exists(p)
    with open(p, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if new:
            writer.writerow(['url','title','text','subject','date','target_csv','scrape_mode','cleaning_status','error','timestamp'])
        snippet = (title[:100] + '...') if title else ''
        writer.writerow([url, title, snippet, subject, date, target, mode, cleaning_status, error or '', datetime.utcnow().isoformat()])

def scrape_url(url, target='true.csv', delay_min=2, delay_max=4, save_raw=True):
    ruleset = load_rules()
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.','')
    rules = ruleset.get(domain, {})
    try:
        raw = fetch_html(url)
    except Exception as e:
        log_scrape(url, '', '', '', target, 'error', 'failed', str(e))
        return {'url':url,'status':'error','error':str(e)}
    if save_raw:
        os.makedirs(SCRAPED_DIR, exist_ok=True)
        fn = os.path.join(SCRAPED_DIR, f"raw_{int(time.time())}.html")
        try:
            with open(fn, 'wb') as f: f.write(raw)
        except Exception:
            pass
    soup = BeautifulSoup(raw, 'html.parser')
    if rules:
        title, content, subject, date = parse_with_rules(soup, rules)
        mode = 'custom'
    else:
        title, content, subject, date = fallback_parse(soup)
        mode = 'fallback'
    cleaned = clean_html_text(content)
    save_article_csv(target, title, cleaned, subject, date or datetime.utcnow().date().isoformat())
    log_scrape(url, title, subject, date, target, mode, 'cleaned')
    time.sleep(random.uniform(delay_min, delay_max))
    return {'url':url,'status':'ok','mode':mode}

def scrape_multiple(urls, target_csv='true.csv', delay_min=2, delay_max=4):
    results = []
    for u in urls:
        results.append(scrape_url(u.strip(), target=target_csv, delay_min=delay_min, delay_max=delay_max))
    return results
