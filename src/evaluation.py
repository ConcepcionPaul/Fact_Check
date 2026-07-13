from training import train_or_load
from preprocessing import tokenize
from bow import vectorize_documents

def compute_metrics(y_true, y_pred):
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
    return {'accuracy':accuracy,'precision':precision,'recall':recall,'f1':f1}

def evaluate_seed(seed=42):
    info = train_or_load(seed=seed)
    model = info['model_obj']; vocab = info['vocab_obj']; test = info['test']
    y_true=[]; y_pred=[]
    for title,text,combined,label in test:
        toks = tokenize(combined)
        vec = vectorize_documents(vocab, [toks])[0]
        pred,conf = model.predict(vec)
        y_true.append(label); y_pred.append(pred)
    return compute_metrics(y_true, y_pred)

def evaluate_or_load(seed=42):
    return evaluate_seed(seed=seed)
