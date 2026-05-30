from dataclasses import dataclass


@dataclass
class EligibilityResult:
    scheme: object
    eligible: bool
    matched: list
    missing: list

    @property
    def score(self):
        total = len(self.matched) + len(self.missing)
        if total == 0:
            return 100
        return round((len(self.matched) / total) * 100)

    @property
    def status(self):
        if self.eligible:
            return "Eligible"
        if self.score >= 75:
            return "Almost eligible"
        return "Not eligible"


def _check_list(value, allowed, label, matched, missing):
    if not allowed or value in allowed:
        matched.append(label)
    else:
        missing.append(label)


def evaluate_scheme(profile, scheme):
    matched = []
    missing = []

    _check_list(profile.domicile_state, scheme.eligible_states, "Domicile/state requirement", matched, missing)
    _check_list(profile.education_level, scheme.education_levels, "Education level requirement", matched, missing)
    _check_list(profile.category, scheme.categories, "Category requirement", matched, missing)
    _check_list(profile.gender, scheme.genders, "Gender requirement", matched, missing)
    _check_list(profile.institution_type, scheme.institution_types, "Institution type requirement", matched, missing)
    _check_list(profile.course_stream, scheme.course_streams, "Course stream requirement", matched, missing)

    if scheme.max_annual_income is None or profile.annual_family_income <= scheme.max_annual_income:
        matched.append("Family income limit")
    else:
        missing.append("Family income limit")

    if scheme.min_marks_percent is None or profile.marks_percent >= scheme.min_marks_percent:
        matched.append("Minimum marks requirement")
    else:
        missing.append("Minimum marks requirement")

    if scheme.min_age is None or profile.age >= scheme.min_age:
        matched.append("Minimum age requirement")
    else:
        missing.append("Minimum age requirement")

    if scheme.max_age is None or profile.age <= scheme.max_age:
        matched.append("Maximum age requirement")
    else:
        missing.append("Maximum age requirement")

    if not scheme.disability_required or profile.has_disability:
        matched.append("Disability condition")
    else:
        missing.append("Disability condition")

    if not scheme.orphan_required or profile.is_orphan:
        matched.append("Orphan/special support condition")
    else:
        missing.append("Orphan/special support condition")

    if not scheme.bpl_required or profile.is_bpl:
        matched.append("BPL condition")
    else:
        missing.append("BPL condition")

    if not scheme.bank_account_required or profile.has_bank_account:
        matched.append("Bank account requirement")
    else:
        missing.append("Bank account requirement")

    if not scheme.aadhaar_linked_bank_required or profile.aadhaar_linked_bank:
        matched.append("Aadhaar-linked bank requirement")
    else:
        missing.append("Aadhaar-linked bank requirement")

    if not scheme.income_certificate_required or profile.has_income_certificate:
        matched.append("Income certificate requirement")
    else:
        missing.append("Income certificate requirement")

    if not scheme.caste_certificate_required or profile.has_caste_certificate:
        matched.append("Caste/category certificate requirement")
    else:
        missing.append("Caste/category certificate requirement")

    if not scheme.disability_certificate_required or profile.has_disability_certificate:
        matched.append("Disability certificate requirement")
    else:
        missing.append("Disability certificate requirement")

    if not scheme.previous_year_pass_required or profile.previous_year_passed:
        matched.append("Previous year pass/renewal requirement")
    else:
        missing.append("Previous year pass/renewal requirement")

    if profile.residence_type == "hosteller" and not scheme.hosteller_allowed:
        missing.append("Hosteller eligibility")
    else:
        matched.append("Hosteller eligibility")

    if profile.residence_type == "day_scholar" and not scheme.day_scholar_allowed:
        missing.append("Day scholar eligibility")
    else:
        matched.append("Day scholar eligibility")

    return EligibilityResult(
        scheme=scheme,
        eligible=not missing,
        matched=matched,
        missing=missing,
    )


def evaluate_all(profile, schemes):
    results = [evaluate_scheme(profile, scheme) for scheme in schemes]
    return sorted(results, key=lambda item: (item.eligible, item.score), reverse=True)
