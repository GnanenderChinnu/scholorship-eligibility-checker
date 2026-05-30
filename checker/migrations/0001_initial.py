from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Scheme",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("provider", models.CharField(max_length=140)),
                ("scope", models.CharField(choices=[("central", "Central Government"), ("state", "State Government")], max_length=20)),
                ("description", models.TextField()),
                ("benefit", models.CharField(max_length=220)),
                ("official_url", models.URLField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("eligible_states", models.JSONField(blank=True, default=list, help_text="Empty means all India")),
                ("education_levels", models.JSONField(blank=True, default=list, help_text="Empty means all levels")),
                ("categories", models.JSONField(blank=True, default=list, help_text="Empty means all categories")),
                ("genders", models.JSONField(blank=True, default=list, help_text="Empty means all genders")),
                ("max_annual_income", models.PositiveIntegerField(blank=True, null=True)),
                ("min_marks_percent", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("disability_required", models.BooleanField(default=False)),
                ("orphan_required", models.BooleanField(default=False)),
                ("bpl_required", models.BooleanField(default=False)),
                ("bank_account_required", models.BooleanField(default=True)),
                ("documents_required", models.TextField(blank=True)),
                ("application_steps", models.TextField(blank=True)),
                ("deadline_note", models.CharField(blank=True, max_length=160)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="StudentProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120)),
                ("date_of_birth", models.DateField()),
                ("gender", models.CharField(choices=[("female", "Female"), ("male", "Male"), ("other", "Other")], max_length=20)),
                ("state", models.CharField(choices=[("andhra_pradesh", "Andhra Pradesh"), ("arunachal_pradesh", "Arunachal Pradesh"), ("assam", "Assam"), ("bihar", "Bihar"), ("chhattisgarh", "Chhattisgarh"), ("goa", "Goa"), ("gujarat", "Gujarat"), ("haryana", "Haryana"), ("himachal_pradesh", "Himachal Pradesh"), ("jharkhand", "Jharkhand"), ("karnataka", "Karnataka"), ("kerala", "Kerala"), ("madhya_pradesh", "Madhya Pradesh"), ("maharashtra", "Maharashtra"), ("manipur", "Manipur"), ("meghalaya", "Meghalaya"), ("mizoram", "Mizoram"), ("nagaland", "Nagaland"), ("odisha", "Odisha"), ("punjab", "Punjab"), ("rajasthan", "Rajasthan"), ("sikkim", "Sikkim"), ("tamil_nadu", "Tamil Nadu"), ("telangana", "Telangana"), ("tripura", "Tripura"), ("uttar_pradesh", "Uttar Pradesh"), ("uttarakhand", "Uttarakhand"), ("west_bengal", "West Bengal"), ("delhi", "Delhi"), ("jammu_kashmir", "Jammu and Kashmir"), ("ladakh", "Ladakh"), ("puducherry", "Puducherry")], max_length=50)),
                ("district", models.CharField(blank=True, max_length=80)),
                ("category", models.CharField(choices=[("general", "General"), ("obc", "OBC"), ("sc", "SC"), ("st", "ST"), ("ews", "EWS"), ("minority", "Minority")], max_length=20)),
                ("religion", models.CharField(blank=True, max_length=60)),
                ("annual_family_income", models.PositiveIntegerField(help_text="Annual income in INR")),
                ("education_level", models.CharField(choices=[("class_9_10", "Class 9-10"), ("class_11_12", "Class 11-12"), ("diploma", "Diploma"), ("undergraduate", "Undergraduate"), ("postgraduate", "Postgraduate"), ("phd", "PhD")], max_length=30)),
                ("course_name", models.CharField(blank=True, max_length=120)),
                ("institution_name", models.CharField(blank=True, max_length=160)),
                ("marks_percent", models.DecimalField(decimal_places=2, max_digits=5)),
                ("has_disability", models.BooleanField(default=False)),
                ("is_orphan", models.BooleanField(default=False)),
                ("is_bpl", models.BooleanField(default=False)),
                ("has_bank_account", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
