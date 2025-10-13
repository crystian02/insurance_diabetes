from rest_framework import serializers

class InsuranceRequest(serializers.Serializer):
    age = serializers.IntegerField(min_value=0)
    bmi = serializers.FloatField(min_value=0)
    children = serializers.IntegerField(min_value=0)
    smoker = serializers.ChoiceField(choices=['yes','no'])
    sex = serializers.ChoiceField(choices=['male','female'])
    region = serializers.ChoiceField(choices=['northeast','northwest','southeast','southwest'])

class InsuranceResponse(serializers.Serializer):
    predicted_cost = serializers.FloatField()

class DiabetesRequest(serializers.Serializer):
    pregnancies = serializers.IntegerField(min_value=0)
    glucose = serializers.FloatField(min_value=0)
    bloodpressure = serializers.FloatField(min_value=0)
    skinthickness = serializers.FloatField(min_value=0)
    insulin = serializers.FloatField(min_value=0)
    bmi = serializers.FloatField(min_value=0)
    dpf = serializers.FloatField(min_value=0)  # DiabetesPedigreeFunction
    age = serializers.IntegerField(min_value=0)

class DiabetesResponse(serializers.Serializer):
    probability = serializers.FloatField()
    prediction = serializers.IntegerField()
    threshold = serializers.FloatField()