## Objetivo del proyecto

Desarrollar un servicio web que integre dos modelos de Machine Learning:
	1) Un modelo de regresión lineal para predecir el costo estimado de un seguro médico.
	2) Un modelo de regresión logística para predecir el riesgo de diabetes.

Ambos modelos fueron entrenados y optimizados utilizando datasets públicos de Kaggle:
	- Medical Insurance Cost – Linear Regression
	- Diabetes Prediction – Logistic Regression

El sistema fue implementado en Django + Scikit-learn, con una interfaz web accesible desde un navegador, permitiendo:
	•	Cargar los modelos en producción.
	•	Realizar predicciones con datos ingresados manualmente.
	•	Mostrar interpretaciones intuitivas de riesgo y costo.
## Ejecución local
cd insurance_diabetes   
python -m venv .venv. --> crear entorno virtual
source .venv/bin/activate  --> activar entorno
venv\Scripts\activate en Windows
pip install -r requirements.txt  --> instalar dependencias 
python manage.py runserver --> iniciar ejecución
Abrir en el navegador:
👉 http://127.0.0.1:8000

## 1. Umbral ideal para el modelo de predicción de diabetes

El modelo de regresión logística predice probabilidades de padecer diabetes.
El umbral predeterminado (threshold = 0.5) divide los resultados entre:
	Clase 0: sin riesgo (probabilidad < 0.5)
	Clase 1: con riesgo (probabilidad ≥ 0.5)

Se probó optimizar este umbral según la métrica ROC-AUC y el F1-Score en el conjunto de validación.

## 2. Factores que más influyen en el costo del seguro médico

El modelo de regresión lineal analiza las variables del dataset insurance.csv.
Mediante RandomForestRegressor (feature_importances_), se identificaron los factores más influyentes:

Variable   | Importancia (%)
-----------|---------------
smoker_yes | 61.9%
bmi        | 21.1%
age        | 13.0%
children   | 1.8%
sex_male   | 0.5%
region     | <0.5%

Conclusión:
El costo del seguro está fuertemente influenciado por el tabaquismo, seguido del IMC (sobrepeso/obesidad) y la edad.
          
## 3. Análisis comparativo con RandomForest

Se utilizó RandomForestRegressor y RandomForestClassifier para comparar desempeño con los modelos base.

Modelo               | Tipo     | Métrica   | Valor
---------------------|----------|-----------|-------
Linear Regression    | Costos   | R²        | 0.97
RandomForest         | Costos   | R²        | 0.99
Logistic Regression  | Diabetes | ROC-AUC   | 0.84
RandomForest         | Diabetes | ROC-AUC   | 1.00

Conclusión:
Los modelos RandomForest presentan mayor capacidad predictiva, aunque con riesgo de sobreajuste (overfitting) en datasets pequeños.

## 4. Técnica de optimización aplicada

Se aplicó GridSearchCV y cross-validation para optimizar hiperparámetros:

🔹Seguro médico (Ridge Regression)
 --> param_grid = {'model__alpha': [0.01, 0.1, 1, 10]}

Mejor parámetro: alpha = 0.1
Mejora MAE ≈ 8.5%

🔹 Diabetes (Logistic Regression)

--> param_grid = {'clf__C': [0.01, 0.1, 1, 10], 'clf__penalty': ['l2']}

Mejor parámetro: C = 0.1
Mejora ROC-AUC ≈ 4%

## Contexto de los datos

Registros | Variables | Descripción
----------|-----------|-------------------------------------------------------------------------------------
1338      | 7         | Predice costo de seguro según edad, IMC, hijos, tabaquismo, sexo y región.
768       | 8         | Mide riesgo de diabetes según glucosa, insulina, IMC, edad y antecedentes.

Los datos fueron limpiados y escalados con StandardScaler y OneHotEncoder para compatibilidad con los pipelines de scikit-learn.

## Sesgo de los modelos
El dataset de diabetes está desbalanceado (35% positivos vs 65% negativos).
Esto puede hacer que el modelo tienda a predecir “no tiene diabetes” con más frecuencia.
	-	Solución: aplicar SMOTE o ajustar el umbral para mayor sensibilidad.
	-   En seguros médicos, el sesgo está relacionado con el tabaquismo:
la mayoría de los no fumadores tienen costos bajos, haciendo que el modelo sobreajuste en esa clase.

Mitigaciones:
	•	Usar validación estratificada (StratifiedKFold).
	•	Evaluar métricas balanceadas (Precision-Recall).
	•	Monitorear fairness si se despliega en producción.
