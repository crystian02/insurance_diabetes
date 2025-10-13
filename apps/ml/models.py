from django.db import models

class Run(models.Model):
    TASKS = (('insurance','Insurance'), ('diabetes','Diabetes'))
    KIND  = (('train','Train'), ('opt','Optimize'), ('rf','RFCompare'))
    task = models.CharField(max_length=16, choices=TASKS)
    kind = models.CharField(max_length=16, choices=KIND)
    params = models.JSONField(default=dict)
    metrics = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task} ({self.kind})"

class PredictionLog(models.Model):
    task = models.CharField(max_length=16)
    payload = models.JSONField()
    prediction = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task} @ {self.created_at}"