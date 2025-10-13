import numpy as np
from sklearn.metrics import f1_score, precision_recall_curve

def optimal_threshold_by_f1(y_true, proba):
    thresholds = np.linspace(0.05, 0.95, 19)
    f1s = [f1_score(y_true, (proba>=t).astype(int)) for t in thresholds]
    i = int(np.argmax(f1s))
    return float(thresholds[i]), float(f1s[i])

def threshold_from_precision_recall(y_true, proba, target='recall', level=0.80):
    prec, rec, thr = precision_recall_curve(y_true, proba)
    if target == 'recall':
        for t, r in zip(thr, rec[1:]):
            if r >= level:
                return float(t)
    return 0.5