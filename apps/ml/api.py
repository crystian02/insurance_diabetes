from rest_framework.views import APIView
from rest_framework.response import Response
import joblib
import pandas as pd
from pathlib import Path

PIPE_DIR = Path("apps/ml/pipelines")


# Predicción de SEGURO MÉDICO

class PredictInsurance(APIView):
    def post(self, request):
        data = request.data
        pipe = joblib.load(PIPE_DIR / "insurance_pipeline.pkl")

        # Crear DataFrame con las columnas exactas que el modelo espera
        df = pd.DataFrame([{
            "age": float(data["age"]),
            "bmi": float(data["bmi"]),
            "children": int(data["children"]),
            "sex": data["sex"],
            "smoker": data["smoker"],
            "region": data["region"],
        }])

        cost = float(pipe.predict(df)[0])
        return Response({"predicted_cost": round(cost, 2)})



#  Predicción de DIABETES

class PredictDiabetes(APIView):
    def post(self, request):
        data = request.data
        pipe = joblib.load(PIPE_DIR / "diabetes_pipeline.pkl")

        df = pd.DataFrame([{
            "Pregnancies": int(data.get("pregnancies", 0)),
            "Glucose": float(data["glucose"]),
            "BloodPressure": float(data["bloodpressure"]),
            "SkinThickness": float(data["skinthickness"]),
            "Insulin": float(data["insulin"]),
            "BMI": float(data["bmi"]),
            "DiabetesPedigreeFunction": float(data["dpf"]),
            "Age": int(data["age"]),
        }])

        prob = float(pipe.predict_proba(df)[0][1])
        pred = int(pipe.predict(df)[0])
        return Response({
            "probability": prob,
            "prediction": pred,
            "threshold": 0.5
        })