import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, mean_absolute_error, roc_auc_score

# ---- Insurance ----
INS_CAT = ['sex','smoker','region']
INS_NUM = ['age','bmi','children']

def rf_insurance(df: pd.DataFrame):
    y = df['charges']
    X = pd.get_dummies(df.drop(columns=['charges']), columns=INS_CAT, drop_first=True)
    rf = RandomForestRegressor(n_estimators=300, random_state=42)
    rf.fit(X, y)
    yhat = rf.predict(X)
    importances = dict(zip(X.columns, rf.feature_importances_))
    return {
        'r2': float(r2_score(y, yhat)), 'mae': float(mean_absolute_error(y, yhat)),
        'importances': sorted(importances.items(), key=lambda kv: kv[1], reverse=True)
    }

# ---- Diabetes ----
FEAT = ['pregnancies','glucose','bloodpressure','skinthickness','insulin','bmi','diabetespedigreefunction','age']
TARGET_CANON = 'outcome'
ALIAS_MAP = {
    'class': TARGET_CANON,
    'diabetes': TARGET_CANON,
    'target': TARGET_CANON,
    'outcome ': TARGET_CANON,
}

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={k: v for k, v in ALIAS_MAP.items() if k in df.columns})
    return df

def rf_diabetes(df: pd.DataFrame):
    df = _normalize_columns(df)
    y = df[TARGET_CANON]
    X = df[FEAT]
    rf = RandomForestClassifier(n_estimators=400, class_weight='balanced', random_state=42)
    rf.fit(X, y)
    proba = rf.predict_proba(X)[:,1]
    importances = dict(zip(FEAT, rf.feature_importances_))
    return {
        'roc_auc': float(roc_auc_score(y, proba)),
        'importances': sorted(importances.items(), key=lambda kv: kv[1], reverse=True)
    }