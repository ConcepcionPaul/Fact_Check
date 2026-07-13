from training import train_or_load
from preprocessing import tokenize
from bow import vectorize_documents
from config import DEFAULT_SEEDS

def verify_input(title, text, seeds=None):
    if seeds is None:
        seeds = DEFAULT_SEEDS
    results = []
    for s in seeds:
        info = train_or_load(seed=s)
        model = info['model_obj']; vocab = info['vocab_obj']
        combined = (title or '') + ' ' + (text or '')
        toks = tokenize(combined)
        vec = vectorize_documents(vocab, [toks])[0]
        pred, conf = model.predict(vec)
        results.append({'seed':s,'pred':pred,'conf':conf})
    preds = [r['pred'] for r in results]
    avg_conf = sum(r['conf'] for r in results)/len(results)
    if all(p==preds[0] for p in preds):
        return {'status':'CONFIDENT','prediction':preds[0],'confidence':avg_conf,'details':results}
    else:
        return {'status':'INCONSISTENT','predictions':results,'message':'⚠️ Inconsistent prediction — models disagree.'}
