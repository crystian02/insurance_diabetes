from django.core.management.base import BaseCommand
import pandas as pd
from apps.ml.services.optimize import optimize_insurance, optimize_diabetes
from apps.ml.models import Run

class Command(BaseCommand):
    help = "Optimiza ambos modelos con GridSearchCV"
    def add_arguments(self, parser):
        parser.add_argument("--insurance", default="data/insurance.csv")
        parser.add_argument("--diabetes", default="data/diabetes.csv")
    def handle(self, *args, **opts):
        df_i = pd.read_csv(opts["insurance"])
        df_d = pd.read_csv(opts["diabetes"])
        oi = optimize_insurance(df_i)
        od = optimize_diabetes(df_d)
        Run.objects.create(task="insurance", kind="opt", metrics=oi)
        Run.objects.create(task="diabetes", kind="opt", metrics=od)
        self.stdout.write(self.style.SUCCESS(f"OPT insurance {oi}"))
        self.stdout.write(self.style.SUCCESS(f"OPT diabetes {od}"))