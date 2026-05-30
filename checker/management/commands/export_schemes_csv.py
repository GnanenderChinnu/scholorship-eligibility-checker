import csv

from django.core.management.base import BaseCommand

from checker.models import Scheme


class Command(BaseCommand):
    help = "Export schemes to a CSV file for review or handoff."

    def add_arguments(self, parser):
        parser.add_argument("path", help="Output CSV path")

    def handle(self, *args, **options):
        fields = [
            "name",
            "provider",
            "scope",
            "description",
            "benefit",
            "official_url",
            "is_active",
            "max_annual_income",
            "min_marks_percent",
            "academic_year",
            "source_url",
            "last_verified_on",
        ]
        with open(options["path"], "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for scheme in Scheme.objects.order_by("name"):
                writer.writerow({field: getattr(scheme, field) for field in fields})
        self.stdout.write(self.style.SUCCESS(f"Exported {Scheme.objects.count()} schemes."))
