from django.urls import path
from . import views
from .api import PredictInsurance, PredictDiabetes

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/predict_insurance', PredictInsurance.as_view()),
    path('api/predict_diabetes', PredictDiabetes.as_view()),
]