import pickle, os
from collections import defaultdict

class Vocabulary:
    def __init__(self):
        self.token2idx = {}
        self.freq = {}

    def build(self, documents, min_freq=1):
        freq = defaultdict(int)
        for doc in documents:
            for t in doc:
                freq[t] += 1
        tokens = [t for t,c in freq.items() if c>=min_freq]
        tokens.sort(key=lambda x: (-freq[x], x))
        self.token2idx = {t:i for i,t in enumerate(tokens)}
        self.freq = {t:freq[t] for t in tokens}

    def save(self, path):
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path,'wb') as f:
            pickle.dump({'token2idx':self.token2idx,'freq':self.freq}, f)

    def load(self, path):
        with open(path,'rb') as f:
            obj = pickle.load(f)
        self.token2idx = obj.get('token2idx',{})
        self.freq = obj.get('freq',{})

    def vocab_size(self):
        return len(self.token2idx)

def vectorize_documents(vocab, documents):
    vectors = []
    V = vocab.vocab_size()
    for doc in documents:
        vec = [0]*V
        for t in doc:
            idx = vocab.token2idx.get(t)
            if idx is not None:
                vec[idx] += 1
        vectors.append(vec)
    return vectors

def export_vocab_csv(vocab, path):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write('token,frequency\n')
        items = sorted(vocab.freq.items(), key=lambda kv: kv[1], reverse=True)
        for t,c in items:
            f.write(f'"{t}",{c}\n')
