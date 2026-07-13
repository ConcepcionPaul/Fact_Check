import os, csv, pickle, random
from datetime import datetime
from preprocessing import tokenize, reload_stopwords
from bow import Vocabulary, vectorize_documents, export_vocab_csv
from naive_bayes import MultinomialNaiveBayes
from config import DATA_DIR, MODELS_DIR, METRICS_HISTORY, TRAINING_LOG, DEFAULT_TRAIN_TEST_SPLIT, MIN_VOCAB_FREQ

def load_dataset():
    data = []
    for fname,label in [('true.csv',0),('false.csv',1)]:
        path = os.path.join(DATA_DIR, fname)
        if not os.path.exists(path): continue
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('title','') or ''
                text = row.get('text','') or ''
                combined = (title + ' ' + text).strip()
                data.append((title,text,combined,label))
    return data

def _paths(seed):
    model = os.path.join(MODELS_DIR, f'model_seed{seed}.pkl')
    vocab = os.path.join(MODELS_DIR, f'vocab_seed{seed}.pkl')
    testp = os.path.join(MODELS_DIR, f'test_seed{seed}.pkl')
    return model, vocab, testp

def train_and_save(seed=42, force_retrain=False):
    os.makedirs(MODELS_DIR, exist_ok=True)
    data = load_dataset()
    if not data:
        raise RuntimeError('No data found in data/ — place true.csv and false.csv (headers only if empty).')
    model_path, vocab_path, test_path = _paths(seed)
    if (not force_retrain) and os.path.exists(model_path) and os.path.exists(vocab_path) and os.path.exists(test_path):
        model = MultinomialNaiveBayes(); model.load(model_path)
        vocab = Vocabulary(); vocab.load(vocab_path)
        with open(test_path,'rb') as f: test = pickle.load(f)
        return {'model_obj':model,'vocab_obj':vocab,'test':test,'loaded':True,'model_path':model_path}
    rnd = random.Random(seed); rnd.shuffle(data)
    n = len(data); split = int(n * DEFAULT_TRAIN_TEST_SPLIT)
    train = data[:split]; test = data[split:]
    tokens = []; y = []
    for title,text,combined,label in train:
        toks = tokenize(combined)
        tokens.append(toks); y.append(label)
    vocab = Vocabulary(); vocab.build(tokens, min_freq=MIN_VOCAB_FREQ)
    X = vectorize_documents(vocab, tokens)
    model = MultinomialNaiveBayes(); model.fit(X,y)
    model.save(model_path); vocab.save(vocab_path)
    with open(test_path,'wb') as f: pickle.dump(test, f)
    # export vocab inspect
    try:
        export_vocab_csv(vocab, os.path.join(DATA_DIR, f'bow_seed_{seed}.csv'))
    except Exception:
        pass
    # compute metrics
    y_true=[]; y_pred=[]
    for title,text,combined,label in test:
        toks = tokenize(combined)
        vec = vectorize_documents(vocab, [toks])[0]
        pred,conf = model.predict(vec)
        y_true.append(label); y_pred.append(pred)
    tp=fp=tn=fn=0
    for yt,yp in zip(y_true,y_pred):
        if yt==1 and yp==1: tp+=1
        elif yt==0 and yp==1: fp+=1
        elif yt==0 and yp==0: tn+=1
        elif yt==1 and yp==0: fn+=1
    accuracy = (tp+tn)/(tp+tn+fp+fn) if (tp+tn+fp+fn)>0 else 0.0
    precision = tp/(tp+fp) if (tp+fp)>0 else 0.0
    recall = tp/(tp+fn) if (tp+fn)>0 else 0.0
    f1 = (2*precision*recall)/(precision+recall) if (precision+recall)>0 else 0.0
    timestamp = datetime.utcnow().isoformat()
    # append metrics log
    new = not os.path.exists(METRICS_HISTORY)
    with open(METRICS_HISTORY,'a',encoding='utf-8',newline='') as f:
        w = csv.writer(f)
        if new: w.writerow(['timestamp','seed','train_size','test_size','accuracy','precision','recall','f1','model_path','is_best'])
        w.writerow([timestamp, seed, len(train), len(test), f'{accuracy:.6f}', f'{precision:.6f}', f'{recall:.6f}', f'{f1:.6f}', model_path, '0'])
    newt = not os.path.exists(TRAINING_LOG)
    with open(TRAINING_LOG,'a',encoding='utf-8',newline='') as f:
        w = csv.writer(f)
        if newt: w.writerow(['timestamp','seed','train_samples','test_samples','vocab_size','accuracy','precision','recall','f1'])
        w.writerow([timestamp, seed, len(train), len(test), vocab.vocab_size(), f'{accuracy:.6f}', f'{precision:.6f}', f'{recall:.6f}', f'{f1:.6f}'])
    return {'model_obj':model,'vocab_obj':vocab,'test':test,'model_path':model_path,'vocab_path':vocab_path,'metrics':{'accuracy':accuracy,'precision':precision,'recall':recall,'f1':f1}, 'loaded':False}

def train_or_load(seed=42, retrain=False):
    return train_and_save(seed=seed, force_retrain=retrain)
