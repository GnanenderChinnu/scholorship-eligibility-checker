from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .eligibility import evaluate_all
from .forms import RegisterForm, StudentProfileForm
from .models import CATEGORY_CHOICES, EDUCATION_LEVEL_CHOICES, STATE_CHOICES, Scheme, StudentProfile


def home(request):
    total_schemes = Scheme.objects.filter(is_active=True).count()
    central_count = Scheme.objects.filter(is_active=True, scope="central").count()
    state_count = Scheme.objects.filter(is_active=True, scope="state").count()
    return render(
        request,
        "checker/home.html",
        {"total_schemes": total_schemes, "central_count": central_count, "state_count": state_count},
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. Add your profile to check eligibility.")
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    profile_exists = StudentProfile.objects.filter(user=request.user).exists()
    matched_count = 0
    almost_count = 0
    total_schemes = Scheme.objects.filter(is_active=True).count()
    if profile_exists:
        profile = request.user.studentprofile
        results = evaluate_all(profile, Scheme.objects.filter(is_active=True))
        matched_count = len([item for item in results if item.eligible])
        almost_count = len([item for item in results if not item.eligible and item.score >= 75])
    return render(
        request,
        "checker/dashboard.html",
        {
            "profile_exists": profile_exists,
            "matched_count": matched_count,
            "almost_count": almost_count,
            "total_schemes": total_schemes,
        },
    )


@login_required
def profile(request):
    instance = StudentProfile.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = StudentProfileForm(request.POST, instance=instance)
        if form.is_valid():
            student_profile = form.save(commit=False)
            student_profile.user = request.user
            student_profile.save()
            messages.success(request, "Profile saved. Your scholarship results are ready.")
            return redirect("results")
    else:
        form = StudentProfileForm(instance=instance)
    return render(request, "checker/profile.html", {"form": form})


@login_required
def results(request):
    profile_obj = StudentProfile.objects.filter(user=request.user).first()
    if not profile_obj:
        messages.info(request, "Add your profile details first.")
        return redirect("profile")
    scheme_results = evaluate_all(profile_obj, Scheme.objects.filter(is_active=True))
    return render(request, "checker/results.html", {"profile": profile_obj, "scheme_results": scheme_results})


def scheme_list(request):
    schemes = Scheme.objects.filter(is_active=True)
    scope = request.GET.get("scope")
    state = request.GET.get("state")
    category = request.GET.get("category")
    education = request.GET.get("education")
    q = request.GET.get("q", "").strip()

    if scope in {"central", "state"}:
        schemes = schemes.filter(scope=scope)
    if q:
        schemes = schemes.filter(Q(name__icontains=q) | Q(provider__icontains=q) | Q(description__icontains=q))

    scheme_list_items = list(schemes)
    if state:
        scheme_list_items = [scheme for scheme in scheme_list_items if not scheme.eligible_states or state in scheme.eligible_states]
    if category:
        scheme_list_items = [scheme for scheme in scheme_list_items if not scheme.categories or category in scheme.categories]
    if education:
        scheme_list_items = [
            scheme for scheme in scheme_list_items if not scheme.education_levels or education in scheme.education_levels
        ]

    filters = {
        "scope": scope or "",
        "state": state or "",
        "category": category or "",
        "education": education or "",
        "q": q,
    }
    return render(
        request,
        "checker/scheme_list.html",
        {
            "schemes": scheme_list_items,
            "filters": filters,
            "state_choices": STATE_CHOICES,
            "category_choices": CATEGORY_CHOICES,
            "education_choices": EDUCATION_LEVEL_CHOICES,
        },
    )


def scheme_detail(request, slug):
    scheme = get_object_or_404(Scheme, slug=slug, is_active=True)
    return render(request, "checker/scheme_detail.html", {"scheme": scheme})


def privacy(request):
    return render(request, "checker/privacy.html")


def terms(request):
    return render(request, "checker/terms.html")
