# apps/ml/services/training_diabetes.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, f1_score
import joblib
from pathlib import Path

FEATURES = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
TARGET   = 'outcome'

def train_diabetes(csv_path: str, out_path: Path) -> dict:
    df = pd.read_csv(csv_path)
    X = df[FEATURES]
    y = df[TARGET]

    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=400, solver='liblinear', random_state=42))
    ])
    pipe.fit(X, y)
    p = pipe.predict_proba(X)[:,1]
    metrics = {'roc_auc': float(roc_auc_score(y, p)), 'f1@0.5': float(f1_score(y, (p>=0.5).astype(int)))}
    out_path.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, out_path / 'diabetes_pipeline.pkl')
    return metrics