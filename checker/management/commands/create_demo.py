from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from checker.models import StudentProfile


class Command(BaseCommand):
    help = "Create a demo student account with a complete profile."

    def handle(self, *args, **options):
        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username="demo_student",
            defaults={"email": "demo@example.com"},
        )
        user.set_password("Demo@12345")
        user.save()

        StudentProfile.objects.update_or_create(
            user=user,
            defaults={
                "full_name": "Demo Student",
                "date_of_birth": date(2005, 6, 15),
                "gender": "female",
                "state": "telangana",
                "domicile_state": "telangana",
                "district": "Hyderabad",
                "category": "sc",
                "religion": "Hindu",
                "annual_family_income": 180000,
                "education_level": "undergraduate",
                "course_name": "B.Tech Computer Science",
                "course_stream": "engineering",
                "current_year": 1,
                "institution_type": "government",
                "institution_name": "Demo Engineering College",
                "marks_percent": 82,
                "previous_year_passed": True,
                "residence_type": "day_scholar",
                "has_disability": False,
                "is_orphan": False,
                "is_bpl": True,
                "has_bank_account": True,
                "aadhaar_linked_bank": True,
                "has_income_certificate": True,
                "has_caste_certificate": True,
                "has_disability_certificate": False,
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo account ready: demo_student / Demo@12345"))
