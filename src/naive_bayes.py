import math, pickle, os
class MultinomialNaiveBayes:
    def __init__(self, alpha=1.0):
        self.alpha = float(alpha)
        self.class_priors = {}
        self.feature_log_prob = {}
        self.classes = []
        self.vocab_size = 0

    def fit(self, X, y):
        label_counts = {}
        feature_counts = {}
        total = len(y)
        self.classes = sorted(set(y))
        self.vocab_size = len(X[0]) if X else 0
        for c in self.classes:
            label_counts[c] = 0
            feature_counts[c] = [0]*self.vocab_size
        for xi, yi in zip(X,y):
            label_counts[yi] += 1
            for i, count in enumerate(xi):
                feature_counts[yi][i] += count
        # priors
        self.class_priors = {c: math.log((label_counts[c]+1)/(total+len(self.classes))) for c in self.classes}
        self.feature_log_prob = {}
        for c in self.classes:
            smoothed = [(feature_counts[c][i] + self.alpha) for i in range(self.vocab_size)]
            denom = sum(smoothed)
            self.feature_log_prob[c] = [math.log(p/denom) for p in smoothed]

    def predict_log_proba(self,x):
        scores = {}
        for c in self.classes:
            score = self.class_priors.get(c, float('-inf'))
            flp = self.feature_log_prob.get(c, [])
            s = 0.0
            for i,count in enumerate(x):
                if i < len(flp):
                    s += count * flp[i]
            scores[c] = score + s
        return scores

    def predict(self,x):
        log_scores = self.predict_log_proba(x)
        max_log = max(log_scores.values())
        exps = {c: math.exp(log_scores[c]-max_log) for c in log_scores}
        s = sum(exps.values())
        probs = {c: exps[c]/s for c in exps}
        pred = max(probs.items(), key=lambda kv: kv[1])[0]
        return int(pred), float(probs[pred])

    def save(self,path):
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path,'wb') as f:
            pickle.dump({'alpha':self.alpha,'class_priors':self.class_priors,'feature_log_prob':self.feature_log_prob,'classes':self.classes,'vocab_size':self.vocab_size}, f)

    def load(self,path):
        with open(path,'rb') as f:
            obj = pickle.load(f)
        self.alpha = obj.get('alpha',1.0)
        self.class_priors = obj.get('class_priors',{})
        self.feature_log_prob = obj.get('feature_log_prob',{})
        self.classes = obj.get('classes',[])
        self.vocab_size = obj.get('vocab_size',0)
