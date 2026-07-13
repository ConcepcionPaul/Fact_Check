from verifier import verify_input
from scraper import scrape_url, scrape_multiple
from ocr_reader import ocr_extract

def classify_text(title, text):
    res = verify_input(title, text)
    if res.get('status')=='CONFIDENT':
        return ('REAL' if res['prediction']==0 else 'FAKE'), res['confidence']
    else:
        return 'INCONSISTENT', 0.0

def classify_url(url):
    out = scrape_url(url, target='true.csv')
    if out.get('status')!='ok':
        return 'INCONSISTENT', 0.0
    import csv, os
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'true.csv')
    try:
        with open(path,'r',encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
            if not rows: return 'INCONSISTENT', 0.0
            last = rows[-1]
            title = last.get('title',''); text = last.get('text','')
            return classify_text(title, text)
    except Exception:
        return 'INCONSISTENT', 0.0

def classify_image(path):
    title, body = ocr_extract(path)
    return classify_text(title, body)
