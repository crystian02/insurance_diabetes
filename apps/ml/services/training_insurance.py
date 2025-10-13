import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
from pathlib import Path

CATEG = ['sex','smoker','region']
NUM   = ['age','bmi','children']

def train_insurance(csv_path: str, out_path: Path) -> dict:
    df = pd.read_csv(csv_path)
    y = df['charges']
    X = df.drop(columns=['charges'])

    pre = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), CATEG),
        ('num', StandardScaler(), NUM),
    ])
    model = Ridge(alpha=1.0, random_state=42)
    pipe = Pipeline([('pre', pre), ('model', model)])
    pipe.fit(X, y)

    y_hat = pipe.predict(X)
    metrics = {'r2': float(r2_score(y, y_hat)), 'mae': float(mean_absolute_error(y, y_hat))}
    out_path.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, out_path / 'insurance_pipeline.pkl')
    return metrics