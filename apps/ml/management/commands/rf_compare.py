from django.core.management.base import BaseCommand
import pandas as pd
from apps.ml.services.rf_compare import rf_insurance, rf_diabetes
from apps.ml.models import Run

class Command(BaseCommand):
    help = "Entrena RF para ambos modelos y reporta importancias"
    def add_arguments(self, parser):
        parser.add_argument("--insurance", default="data/insurance.csv")
        parser.add_argument("--diabetes", default="data/diabetes.csv")
    def handle(self, *args, **opts):
        di = pd.read_csv(opts["insurance"])
        dd = pd.read_csv(opts["diabetes"])
        ri = rf_insurance(di)
        rd = rf_diabetes(dd)
        Run.objects.create(task="insurance", kind="rf", metrics=ri)
        Run.objects.create(task="diabetes", kind="rf", metrics=rd)
        self.stdout.write(self.style.SUCCESS(f"RF insurance {ri}"))
        self.stdout.write(self.style.SUCCESS(f"RF diabetes {rd}"))