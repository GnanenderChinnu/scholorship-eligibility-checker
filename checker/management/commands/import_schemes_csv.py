import csv

from django.core.management.base import BaseCommand, CommandError

from checker.models import Scheme


class Command(BaseCommand):
    help = "Import basic scheme data from CSV. Existing rows are matched by scheme name."

    def add_arguments(self, parser):
        parser.add_argument("path", help="Input CSV path")

    def handle(self, *args, **options):
        required = {"name", "provider", "scope", "description", "benefit"}
        created = 0
        updated = 0
        with open(options["path"], newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"Missing required columns: {', '.join(sorted(missing))}")

            for row in reader:
                name = row.pop("name").strip()
                if not name:
                    continue
                clean_row = {key: value for key, value in row.items() if value not in {None, ""}}
                if "is_active" in clean_row:
                    clean_row["is_active"] = clean_row["is_active"].lower() in {"1", "true", "yes"}
                scheme, was_created = Scheme.objects.update_or_create(name=name, defaults=clean_row)
                scheme.full_clean()
                scheme.save()
                created += int(was_created)
                updated += int(not was_created)

        self.stdout.write(self.style.SUCCESS(f"Imported schemes: {created} created, {updated} updated."))
