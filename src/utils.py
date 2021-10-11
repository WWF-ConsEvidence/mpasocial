import re
from api.models import Household, MPAInterviewYear


def is_match(string, match_patterns):
    for match_pattern in match_patterns:
        if re.search(match_pattern, string) is not None:
            return True
    return False


def truthy(val):
    return val in ("t", "T", "true", "True", True, 1)


def upsert_mpa_interviewyear(mpa, year):
    my, created = MPAInterviewYear.objects.get_or_create(mpa=mpa, year=year)
    return my, created


def populate_mpa_interviewyears(*args):
    households = Household.objects.all()
    for household in households:
        upsert_mpa_interviewyear(household.mpa, household.interviewyear)
