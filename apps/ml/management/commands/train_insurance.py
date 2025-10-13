from django.core.management.base import BaseCommand
from pathlib import Path
from apps.ml.services.training_insurance import train_insurance
from apps.ml.models import Run

class Command(BaseCommand):
    help = "Entrena el modelo de seguro y guarda pipeline"
    def add_arguments(self, parser):
        parser.add_argument("--csv", default="data/insurance.csv")
    def handle(self, *args, **opts):
        m = train_insurance(opts["csv"], Path("apps/ml/pipelines"))
        Run.objects.create(task="insurance", kind="train", metrics=m)
        self.stdout.write(self.style.SUCCESS(f"OK insurance {m}"))