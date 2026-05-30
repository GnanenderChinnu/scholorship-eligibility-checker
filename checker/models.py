from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


GENDER_CHOICES = [
    ("female", "Female"),
    ("male", "Male"),
    ("other", "Other"),
]

CATEGORY_CHOICES = [
    ("general", "General"),
    ("obc", "OBC"),
    ("sc", "SC"),
    ("st", "ST"),
    ("ews", "EWS"),
    ("minority", "Minority"),
]

EDUCATION_LEVEL_CHOICES = [
    ("class_9_10", "Class 9-10"),
    ("class_11_12", "Class 11-12"),
    ("diploma", "Diploma"),
    ("undergraduate", "Undergraduate"),
    ("postgraduate", "Postgraduate"),
    ("phd", "PhD"),
]

INSTITUTION_TYPE_CHOICES = [
    ("government", "Government"),
    ("aided", "Government Aided"),
    ("private", "Private"),
    ("deemed", "Deemed University"),
]

COURSE_STREAM_CHOICES = [
    ("general", "General"),
    ("technical", "Technical / Professional"),
    ("medical", "Medical"),
    ("engineering", "Engineering"),
    ("vocational", "Vocational"),
    ("research", "Research"),
]

RESIDENCE_TYPE_CHOICES = [
    ("day_scholar", "Day Scholar"),
    ("hosteller", "Hosteller"),
]

STATE_CHOICES = [
    ("andhra_pradesh", "Andhra Pradesh"),
    ("arunachal_pradesh", "Arunachal Pradesh"),
    ("assam", "Assam"),
    ("bihar", "Bihar"),
    ("chhattisgarh", "Chhattisgarh"),
    ("goa", "Goa"),
    ("gujarat", "Gujarat"),
    ("haryana", "Haryana"),
    ("himachal_pradesh", "Himachal Pradesh"),
    ("jharkhand", "Jharkhand"),
    ("karnataka", "Karnataka"),
    ("kerala", "Kerala"),
    ("madhya_pradesh", "Madhya Pradesh"),
    ("maharashtra", "Maharashtra"),
    ("manipur", "Manipur"),
    ("meghalaya", "Meghalaya"),
    ("mizoram", "Mizoram"),
    ("nagaland", "Nagaland"),
    ("odisha", "Odisha"),
    ("punjab", "Punjab"),
    ("rajasthan", "Rajasthan"),
    ("sikkim", "Sikkim"),
    ("tamil_nadu", "Tamil Nadu"),
    ("telangana", "Telangana"),
    ("tripura", "Tripura"),
    ("uttar_pradesh", "Uttar Pradesh"),
    ("uttarakhand", "Uttarakhand"),
    ("west_bengal", "West Bengal"),
    ("delhi", "Delhi"),
    ("jammu_kashmir", "Jammu and Kashmir"),
    ("ladakh", "Ladakh"),
    ("puducherry", "Puducherry"),
]


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    state = models.CharField(max_length=50, choices=STATE_CHOICES)
    domicile_state = models.CharField(max_length=50, choices=STATE_CHOICES, default="telangana")
    district = models.CharField(max_length=80, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    religion = models.CharField(max_length=60, blank=True)
    annual_family_income = models.PositiveIntegerField(help_text="Annual income in INR")
    education_level = models.CharField(max_length=30, choices=EDUCATION_LEVEL_CHOICES)
    course_name = models.CharField(max_length=120, blank=True)
    course_stream = models.CharField(max_length=30, choices=COURSE_STREAM_CHOICES, default="general")
    current_year = models.PositiveSmallIntegerField(default=1)
    institution_type = models.CharField(max_length=30, choices=INSTITUTION_TYPE_CHOICES, default="government")
    institution_name = models.CharField(max_length=160, blank=True)
    marks_percent = models.DecimalField(max_digits=5, decimal_places=2)
    previous_year_passed = models.BooleanField(default=True)
    residence_type = models.CharField(max_length=20, choices=RESIDENCE_TYPE_CHOICES, default="day_scholar")
    has_disability = models.BooleanField(default=False)
    is_orphan = models.BooleanField(default=False)
    is_bpl = models.BooleanField(default=False)
    has_bank_account = models.BooleanField(default=True)
    aadhaar_linked_bank = models.BooleanField(default=False)
    has_income_certificate = models.BooleanField(default=False)
    has_caste_certificate = models.BooleanField(default=False)
    has_disability_certificate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        today = timezone.localdate()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def __str__(self):
        return self.full_name

    def clean(self):
        if self.marks_percent < 0 or self.marks_percent > 100:
            raise ValidationError({"marks_percent": "Marks percentage must be between 0 and 100."})
        if self.current_year < 1:
            raise ValidationError({"current_year": "Current year must be at least 1."})


class Scheme(models.Model):
    SCOPE_CHOICES = [
        ("central", "Central Government"),
        ("state", "State Government"),
    ]

    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    provider = models.CharField(max_length=140)
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES)
    description = models.TextField()
    benefit = models.CharField(max_length=220)
    official_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    eligible_states = models.JSONField(default=list, blank=True, help_text="Empty means all India")
    education_levels = models.JSONField(default=list, blank=True, help_text="Empty means all levels")
    categories = models.JSONField(default=list, blank=True, help_text="Empty means all categories")
    genders = models.JSONField(default=list, blank=True, help_text="Empty means all genders")
    institution_types = models.JSONField(default=list, blank=True, help_text="Empty means all institution types")
    course_streams = models.JSONField(default=list, blank=True, help_text="Empty means all course streams")
    max_annual_income = models.PositiveIntegerField(null=True, blank=True)
    min_marks_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    min_age = models.PositiveSmallIntegerField(null=True, blank=True)
    max_age = models.PositiveSmallIntegerField(null=True, blank=True)
    disability_required = models.BooleanField(default=False)
    orphan_required = models.BooleanField(default=False)
    bpl_required = models.BooleanField(default=False)
    bank_account_required = models.BooleanField(default=True)
    aadhaar_linked_bank_required = models.BooleanField(default=False)
    income_certificate_required = models.BooleanField(default=True)
    caste_certificate_required = models.BooleanField(default=False)
    disability_certificate_required = models.BooleanField(default=False)
    previous_year_pass_required = models.BooleanField(default=True)
    hosteller_allowed = models.BooleanField(default=True)
    day_scholar_allowed = models.BooleanField(default=True)
    documents_required = models.TextField(blank=True)
    application_steps = models.TextField(blank=True)
    deadline_note = models.CharField(max_length=160, blank=True)
    academic_year = models.CharField(max_length=20, default="2025-26")
    source_url = models.URLField(blank=True)
    last_verified_on = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def clean(self):
        allowed_states = {value for value, _ in STATE_CHOICES}
        allowed_levels = {value for value, _ in EDUCATION_LEVEL_CHOICES}
        allowed_categories = {value for value, _ in CATEGORY_CHOICES}
        allowed_genders = {value for value, _ in GENDER_CHOICES}
        allowed_institutions = {value for value, _ in INSTITUTION_TYPE_CHOICES}
        allowed_streams = {value for value, _ in COURSE_STREAM_CHOICES}

        checks = {
            "eligible_states": (self.eligible_states, allowed_states),
            "education_levels": (self.education_levels, allowed_levels),
            "categories": (self.categories, allowed_categories),
            "genders": (self.genders, allowed_genders),
            "institution_types": (self.institution_types, allowed_institutions),
            "course_streams": (self.course_streams, allowed_streams),
        }
        errors = {}
        for field, (values, allowed) in checks.items():
            invalid = [value for value in values if value not in allowed]
            if invalid:
                errors[field] = f"Invalid value(s): {', '.join(invalid)}"

        if self.min_marks_percent is not None and (self.min_marks_percent < 0 or self.min_marks_percent > 100):
            errors["min_marks_percent"] = "Minimum marks must be between 0 and 100."
        if self.min_age and self.max_age and self.min_age > self.max_age:
            errors["max_age"] = "Maximum age must be greater than or equal to minimum age."
        if not self.hosteller_allowed and not self.day_scholar_allowed:
            errors["hosteller_allowed"] = "At least one residence type must be allowed."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 2
            while Scheme.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
