from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import pandas as pd

INS_CATEG = ['sex','smoker','region']
INS_NUM   = ['age','bmi','children']

def optimize_insurance(df: pd.DataFrame):
    # Seguro ya viene con columnas correctas en minúsculas
    y = df['charges']
    X = df.drop(columns=['charges'])
    pre = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), INS_CATEG),
        ('num', StandardScaler(), INS_NUM),
    ])
    pipe = Pipeline([('pre', pre), ('model', Ridge())])
    grid = {'model__alpha':[0.1,0.5,1.0,2.0,5.0,10.0]}
    gs = GridSearchCV(pipe, grid, scoring='neg_mean_absolute_error', cv=5, n_jobs=-1)
    gs.fit(X,y)
    return {'best_params': gs.best_params_, 'best_score_mae': float(-gs.best_score_)}

# ---- Diabetes ----

DIAB_FEAT = ['pregnancies','glucose','bloodpressure','skinthickness','insulin','bmi','diabetespedigreefunction','age']
TARGET_CANON = 'outcome'
ALIAS_MAP = {
    'class': TARGET_CANON,
    'diabetes': TARGET_CANON,
    'target': TARGET_CANON,
    'outcome ': TARGET_CANON,
    'dpf': 'diabetespedigreefunction',
    'diabetespedigreefunc': 'diabetespedigreefunction',
}

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={k: v for k, v in ALIAS_MAP.items() if k in df.columns})
    return df

def optimize_diabetes(df: pd.DataFrame):
    df = _normalize_columns(df)
    missing = set(DIAB_FEAT + [TARGET_CANON]) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas para diabetes: {sorted(missing)}. Tengo: {df.columns.tolist()}")
    X = df[DIAB_FEAT]; y = df[TARGET_CANON]
    pipe = Pipeline([('sc', StandardScaler()), ('clf', LogisticRegression(solver='liblinear', max_iter=500))])
    grid = {'clf__C':[0.1,0.5,1,2,5,10], 'clf__penalty':['l1','l2']}
    gs = GridSearchCV(pipe, grid, scoring='roc_auc', cv=5, n_jobs=-1)
    gs.fit(X,y)
    return {'best_params': gs.best_params_, 'best_score_roc_auc': float(gs.best_score_)}