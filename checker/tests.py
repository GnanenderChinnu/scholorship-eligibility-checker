from datetime import date

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import Client, TestCase

from .eligibility import evaluate_scheme
from .models import Scheme, StudentProfile


class EligibilityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="student", password="pass12345")
        self.profile = StudentProfile.objects.create(
            user=self.user,
            full_name="Test Student",
            date_of_birth=date(2004, 5, 10),
            gender="female",
            state="telangana",
            domicile_state="telangana",
            category="sc",
            annual_family_income=180000,
            education_level="undergraduate",
            course_stream="technical",
            marks_percent=78,
            has_bank_account=True,
            aadhaar_linked_bank=True,
            has_income_certificate=True,
            has_caste_certificate=True,
        )

    def test_scheme_is_eligible_when_all_structured_rules_match(self):
        scheme = Scheme.objects.create(
            name="Matching Scheme",
            provider="Test Provider",
            scope="central",
            description="A matching scholarship.",
            benefit="Fee support",
            eligible_states=["telangana"],
            education_levels=["undergraduate"],
            categories=["sc"],
            genders=["female"],
            course_streams=["technical"],
            max_annual_income=200000,
            min_marks_percent=60,
            caste_certificate_required=True,
            aadhaar_linked_bank_required=True,
        )

        result = evaluate_scheme(self.profile, scheme)

        self.assertTrue(result.eligible)
        self.assertEqual(result.missing, [])

    def test_scheme_reports_missing_rules_when_profile_does_not_match(self):
        scheme = Scheme.objects.create(
            name="Non Matching Scheme",
            provider="Test Provider",
            scope="state",
            description="A restrictive scholarship.",
            benefit="Fee support",
            eligible_states=["karnataka"],
            categories=["st"],
            max_annual_income=100000,
            min_marks_percent=85,
        )

        result = evaluate_scheme(self.profile, scheme)

        self.assertFalse(result.eligible)
        self.assertIn("Domicile/state requirement", result.missing)
        self.assertIn("Category requirement", result.missing)
        self.assertIn("Family income limit", result.missing)
        self.assertIn("Minimum marks requirement", result.missing)

    def test_scheme_validation_rejects_unknown_structured_values(self):
        scheme = Scheme(
            name="Bad Scheme",
            provider="Test Provider",
            scope="central",
            description="Invalid rule values.",
            benefit="None",
            eligible_states=["unknown_state"],
        )

        with self.assertRaises(ValidationError):
            scheme.full_clean()


class PortalFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        Scheme.objects.create(
            name="Searchable Telangana Scheme",
            provider="Portal Provider",
            scope="state",
            description="A searchable scheme.",
            benefit="Fee support",
            eligible_states=["telangana"],
            categories=["sc"],
            education_levels=["undergraduate"],
        )

    def test_scheme_filters_render_matching_scheme(self):
        response = self.client.get(
            "/schemes/",
            {"state": "telangana", "category": "sc", "education": "undergraduate", "q": "Searchable"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Searchable Telangana Scheme")

    def test_profile_submission_redirects_to_results(self):
        user = User.objects.create_user(username="flow", password="pass12345")
        self.client.login(username="flow", password="pass12345")

        response = self.client.post(
            "/profile/",
            {
                "full_name": "Flow Student",
                "date_of_birth": "2005-01-01",
                "gender": "female",
                "state": "telangana",
                "domicile_state": "telangana",
                "district": "Hyderabad",
                "category": "sc",
                "religion": "Hindu",
                "annual_family_income": "180000",
                "education_level": "undergraduate",
                "course_name": "B.Tech",
                "course_stream": "engineering",
                "current_year": "1",
                "institution_type": "government",
                "institution_name": "Flow College",
                "marks_percent": "80",
                "previous_year_passed": "on",
                "residence_type": "day_scholar",
                "is_bpl": "on",
                "has_bank_account": "on",
                "aadhaar_linked_bank": "on",
                "has_income_certificate": "on",
                "has_caste_certificate": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/results/")
        self.assertTrue(StudentProfile.objects.filter(user=user).exists())
