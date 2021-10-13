from django_filters import BaseInFilter, FilterSet, NumberFilter
from .mixins import OrFilterSetMixin


BASE_IN_HELPTEXT = ". Multiple values may be separated by commas."


class BaseAPIFilterSet(OrFilterSetMixin, FilterSet):
    pass
    # created_on = DateTimeFromToRangeFilter()
    # updated_on = DateTimeFromToRangeFilter()
    #
    # class Meta:
    #     fields = ["created_on", "updated_on", "updated_by"]


class BaseFGDFilterSet(BaseAPIFilterSet):
    def fgd_filter(self, queryset, name, value):
        name = f"fgd__fgdid"
        return self.int_lookup(queryset, name, value)

    def treatment_filter(self, queryset, name, value):
        lookup = f"household__settlement__treatment"
        return queryset.filter(**{lookup: value})

    fgd = BaseInFilter(
        method="fgd_filter",
        help_text=f"Integer ID of associated household{BASE_IN_HELPTEXT}",
    )
    treatment = NumberFilter(
        method="treatment_filter",
        help_text=f"Integer ID of associated household survey settlement treatment",
    )


class BaseHouseholdFilterSet(BaseAPIFilterSet):
    def household_filter(self, queryset, name, value):
        name = f"household__householdid"
        return self.int_lookup(queryset, name, value)

    def mpa_filter(self, queryset, name, value):
        name = f"household__settlement__mpa__pk"
        return self.int_lookup(queryset, name, value)

    def interviewyear_filter(self, queryset, name, value):
        name = f"household__yearmonitoring"
        return self.int_lookup(queryset, name, value)

    def seascape_filter(self, queryset, name, value):
        lookup = f"household__settlement__mpa__seascape"
        return queryset.filter(**{lookup: value})

    def treatment_filter(self, queryset, name, value):
        lookup = f"household__settlement__treatment"
        return queryset.filter(**{lookup: value})

    household = BaseInFilter(
        method="household_filter",
        help_text=f"Integer ID of associated household{BASE_IN_HELPTEXT}",
    )
    mpa = BaseInFilter(
        method="mpa_filter",
        help_text=f"Integer ID of associated household survey MPA{BASE_IN_HELPTEXT}",
    )
    yearmonitoring = BaseInFilter(
        method="interviewyear_filter",
        help_text=f"4-digit integer year of associated household survey{BASE_IN_HELPTEXT}",
    )
    seascape = NumberFilter(
        method="seascape_filter",
        help_text=f"Integer ID of associated household survey MPA seascape",
    )
    treatment = NumberFilter(
        method="treatment_filter",
        help_text=f"Integer ID of associated household survey settlement treatment",
    )


class BaseKIIFilterSet(BaseAPIFilterSet):
    def kii_filter(self, queryset, name, value):
        name = f"kii__kiiid"
        return self.int_lookup(queryset, name, value)

    def mpa_filter(self, queryset, name, value):
        name = f"kii__settlement__mpa__pk"
        return self.int_lookup(queryset, name, value)

    def seascape_filter(self, queryset, name, value):
        lookup = f"kii__settlement__mpa__seascape"
        return queryset.filter(**{lookup: value})

    def treatment_filter(self, queryset, name, value):
        lookup = f"kii__settlement__treatment"
        return queryset.filter(**{lookup: value})

    kii = BaseInFilter(
        method="kii_filter", help_text=f"Integer ID of associated KII{BASE_IN_HELPTEXT}"
    )
    mpa = BaseInFilter(
        method="mpa_filter",
        help_text=f"Integer ID of associated KII MPA{BASE_IN_HELPTEXT}",
    )
    seascape = NumberFilter(
        method="seascape_filter", help_text=f"Integer ID of associated KII MPA seascape"
    )
    treatment = NumberFilter(
        method="treatment_filter",
        help_text=f"Integer ID of associated KII settlement treatment",
    )


class FGDFilterSet(BaseAPIFilterSet):
    def treatment_filter(self, queryset, name, value):
        lookup = f"settlement__treatment"
        return queryset.filter(**{lookup: value})

    treatment = NumberFilter(
        method="treatment_filter",
        help_text=f"Integer ID of associated household survey settlement treatment",
    )


class HouseholdKIIFilterSet(BaseAPIFilterSet):
    def mpa_filter(self, queryset, name, value):
        name = f"settlement__mpa__pk"
        return self.int_lookup(queryset, name, value)

    def seascape_filter(self, queryset, name, value):
        lookup = f"settlement__mpa__seascape"
        return queryset.filter(**{lookup: value})

    def treatment_filter(self, queryset, name, value):
        lookup = f"settlement__treatment"
        return queryset.filter(**{lookup: value})

    mpa = BaseInFilter(
        method="mpa_filter", help_text=f"Integer ID of MPA{BASE_IN_HELPTEXT}"
    )
    yearmonitoring = BaseInFilter(
        method="int_lookup", help_text=f"4-digit integer year{BASE_IN_HELPTEXT}"
    )
    seascape = NumberFilter(
        method="seascape_filter", help_text=f"Integer ID of MPA seascape"
    )
    treatment = NumberFilter(
        method="treatment_filter", help_text=f"Integer ID of settlement treatment"
    )
