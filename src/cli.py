import os, csv, time
from datetime import datetime
from config import USER_LOG, SCRAPED_LOG, DEFAULT_SEEDS
from training import train_or_load
from evaluation import evaluate_or_load
from verifier import verify_input
from scraper import scrape_multiple, scrape_url
from ocr_reader import ocr_extract

def ensure_user_log():
    if not os.path.exists(USER_LOG):
        with open(USER_LOG,'w',encoding='utf-8',newline='') as f:
            w = csv.writer(f); w.writerow(['timestamp','title','text','source_link','prediction','confidence','verifier_status'])

def log_user(title,text,source,pred,conf,status):
    ensure_user_log()
    with open(USER_LOG,'a',encoding='utf-8',newline='') as f:
        w = csv.writer(f); w.writerow([datetime.utcnow().isoformat(), title, text, source, pred, f'{conf:.6f}', status])

def menu():
    ensure_user_log()
    while True:
        print('\nMenu:')
        print('1) Train model')
        print('2) Evaluate model')
        print('3) Classify new article (manual/URL/image)')
        print('4) Batch classify from CSV')
        print('5) Scrape news (multiple URLs)')
        print('6) Export Bag-of-Words CSV for last seed')
        print('7) Reload stopwords')
        print('8) Exit')
        ch = input('Choose: ').strip()
        if ch=='1':
            s = input('Enter seed (default 42): ').strip(); seed = int(s) if s else DEFAULT_SEEDS[0]
            train_or_load(seed=seed, retrain=True); print('Training done.')
        elif ch=='2':
            s = input('Enter seed to evaluate (default 42): ').strip(); seed = int(s) if s else DEFAULT_SEEDS[0]
            metrics = evaluate_or_load(seed=seed); print('Metrics:', metrics)
        elif ch=='3':
            m = input('Mode: 1) manual 2) URL 3) image: ').strip()
            if m=='1':
                title = input('Title: '); text = input('Text: ')
                res = verify_input(title, text)
                if res.get('status')=='CONFIDENT':
                    pred = res['prediction']; conf = res['confidence']
                    print('Prediction:', 'fake' if pred==1 else 'real', conf)
                    log_user(title, text, '', 'fake' if pred==1 else 'real', conf, 'CONFIDENT')
                else:
                    print(res.get('message'))
        elif ch=='4':
            p = input('CSV path: ').strip()
            if not os.path.exists(p): print('Not found'); continue
            import csv
            rows=[]
            with open(p,'r',encoding='utf-8') as f:
                r = csv.DictReader(f)
                for row in r:
                    res = verify_input(row.get('title',''), row.get('text',''))
                    rows.append({'title':row.get('title',''),'prediction': 'fake' if res.get('prediction',1)==1 else 'real', 'status':res.get('status'),'confidence':res.get('confidence',0.0)})
            outp = os.path.splitext(p)[0] + '_classified.csv'
            with open(outp,'w',encoding='utf-8',newline='') as f:
                w = csv.DictWriter(f, fieldnames=['title','prediction','status','confidence']); w.writeheader(); [w.writerow(r) for r in rows]
            print('Saved to', outp)
        elif ch=='5':
            txt = input('Enter URLs (comma separated): ').strip()
            urls = [u.strip() for u in txt.split(',') if u.strip()]
            target = input('Target CSV (true.csv/false.csv): ').strip() or 'true.csv'
            results = scrape_multiple(urls, target_csv=target)
            for r in results: print(r)
        elif ch=='6':
            from bow import export_vocab_csv
            import os
            models = os.listdir(os.path.join(os.path.dirname(__file__),'..','models'))
            v = [m for m in models if m.startswith('vocab_seed')]
            if not v: print('No vocab found. Train first.'); continue
            latest = sorted(v)[-1]
            export_vocab_csv_path = os.path.join(os.path.dirname(__file__),'..','data','vocab_export.csv')
            from bow import Vocabulary
            vocab = Vocabulary(); vocab.load(os.path.join(os.path.dirname(__file__),'..','models', latest))
            export_vocab_csv(vocab, export_vocab_csv_path)
            print('Exported to', export_vocab_csv_path)
        elif ch=='7':
            from preprocessing import reload_stopwords
            reload_stopwords(); print('Stopwords reloaded.')
        elif ch=='8':
            print('Exit'); break
        else:
            print('Invalid choice')

if __name__=='__main__':
    menu()
