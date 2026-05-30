from django.contrib import admin

from .models import Scheme, StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "domicile_state", "category", "education_level", "annual_family_income")
    search_fields = ("full_name", "user__username", "district")
    list_filter = ("domicile_state", "category", "education_level", "gender", "course_stream", "has_disability", "is_bpl")


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "scope", "academic_year", "is_active", "max_annual_income", "min_marks_percent", "last_verified_on")
    list_filter = ("scope", "academic_year", "is_active", "disability_required", "orphan_required", "bpl_required")
    search_fields = ("name", "provider", "description")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Basic details", {"fields": ("name", "slug", "provider", "scope", "description", "benefit", "official_url", "is_active")}),
        ("Structured eligibility rules", {"fields": ("eligible_states", "education_levels", "categories", "genders", "institution_types", "course_streams", "max_annual_income", "min_marks_percent", "min_age", "max_age", "disability_required", "orphan_required", "bpl_required", "bank_account_required", "aadhaar_linked_bank_required", "income_certificate_required", "caste_certificate_required", "disability_certificate_required", "previous_year_pass_required", "hosteller_allowed", "day_scholar_allowed")}),
        ("Application information", {"fields": ("documents_required", "application_steps", "deadline_note")}),
        ("Verification", {"fields": ("academic_year", "source_url", "last_verified_on")}),
    )
