from django.core.management.base import BaseCommand
from pathlib import Path
from apps.ml.services.training_diabetes import train_diabetes
from apps.ml.models import Run

class Command(BaseCommand):
    help = "Entrena el modelo de diabetes y guarda pipeline"
    def add_arguments(self, parser):
        parser.add_argument("--csv", default="data/diabetes.csv")
    def handle(self, *args, **opts):
        m = train_diabetes(opts["csv"], Path("apps/ml/pipelines"))
        Run.objects.create(task="diabetes", kind="train", metrics=m)
        self.stdout.write(self.style.SUCCESS(f"OK diabetes {m}"))