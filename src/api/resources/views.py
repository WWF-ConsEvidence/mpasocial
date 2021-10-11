from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from ..reports import csv_report
from .serializers import *
from .filters import (
    BaseHouseholdFilterSet,
    BaseFGDFilterSet,
    BaseKIIFilterSet,
    FGDFilterSet,
    HouseholdKIIFilterSet,
)
from .mixins import MethodAuthenticationMixin
from utils import truthy


class StandardResultPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "limit"
    max_page_size = 5000


class BaseAPIView(MethodAuthenticationMixin, viewsets.ReadOnlyModelViewSet):
    drf_label = ""
    serializer_class_csv = None
    pagination_class = StandardResultPagination

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        order_by = getattr(self, "order_by") if hasattr(self, "order_by") else None
        if order_by:
            qs = qs.order_by(*order_by)

        return qs

    def list(self, request, *args, **kwargs):
        # is_field_report = truthy(request.query_params.get("field_report"))
        show_display_fields = True
        include_additional_fields = True

        queryset = self.filter_queryset(self.get_queryset())
        if self.drf_label == "":
            self.drf_label = queryset.model.__name__.lower()
        file_name_prefix = f"{self.drf_label}"
        if "file_name_prefix" in kwargs:
            file_name_prefix = kwargs["file_name_prefix"]

        return csv_report.get_csv_response(
            queryset,
            self.serializer_class_csv,
            file_name_prefix=file_name_prefix,
            include_additional_fields=include_additional_fields,
            show_display_fields=show_display_fields,
        )

    @action(detail=False, methods=["get"], url_name="json")
    def json(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BaseHouseholdView(BaseAPIView):
    perms_lookup_base = ""

    def limit_to_mpas_interviewyears(self, request, *args, **kwargs):
        mpas = []
        interviewyears = []

        if (
            hasattr(self, "request")
            and hasattr(self.request, "user")
            and self.request.user is not None
        ):
            user = self.request.user
            mpa_interviewyears = list(
                user.profile.mpa_interviewyears.values_list("mpa", "year")
            )
            if len(mpa_interviewyears) > 0:
                mpas, interviewyears = zip(*mpa_interviewyears)

        if self.perms_lookup_base != "":
            self.perms_lookup_base = f"{self.perms_lookup_base}__"
        mpas_interviewyears_filter = {
            f"{self.perms_lookup_base}settlement__mpa__in": mpas,
            f"{self.perms_lookup_base}yearmonitoring__in": interviewyears,
        }
        self.queryset = self.get_queryset().filter(**mpas_interviewyears_filter)

    def list(self, request, *args, **kwargs):
        self.limit_to_mpas_interviewyears(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.limit_to_mpas_interviewyears(request, *args, **kwargs)
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_name="json")
    def json(self, request, *args, **kwargs):
        self.limit_to_mpas_interviewyears(request, *args, **kwargs)
        return super().json(request, *args, **kwargs)


class BaseFGDView(BaseAPIView):
    filterset_class = BaseFGDFilterSet
    order_by = ["fgd__fgyear", "fgd__settlement__pk", "fgd__fgdid", "pk"]


class BaseHouseholdRelatedView(BaseHouseholdView):
    filterset_class = BaseHouseholdFilterSet
    order_by = [
        "household__yearmonitoring",
        "household__settlement__mpa__pk",
        "household__settlement__pk",
        "household__householdid",
        "pk",
    ]


class BaseKIIView(BaseAPIView):
    filterset_class = BaseKIIFilterSet
    order_by = [
        "kii_kiiyear",
        "kii__settlement__mpa__pk",
        "kii__settlement__pk",
        "kii__kiiid",
        "pk",
    ]


class ListBirth(BaseHouseholdRelatedView):
    perms_lookup_base = "household"
    serializer_class = BirthSerializer
    serializer_class_csv = BirthSerializerCSV
    queryset = Birth.objects.select_related(
        "household__settlement__mpa", "household__settlement"
    )


class ListCountry(BaseAPIView):
    serializer_class = CountrySerializer
    serializer_class_csv = CountrySerializerCSV
    order_by = ["name"]
    queryset = Country.objects.all()


class ListDeath(BaseHouseholdRelatedView):
    perms_lookup_base = "household"
    serializer_class = DeathSerializer
    serializer_class_csv = DeathSerializerCSV
    queryset = Death.objects.select_related(
        "household__settlement__mpa", "household__settlement"
    )


class ListDemographic(BaseHouseholdRelatedView):
    perms_lookup_base = "household"
    serializer_class = DemographicSerializer
    serializer_class_csv = DemographicSerializerCSV
    queryset = Demographic.objects.select_related(
        "household__settlement__mpa", "household__settlement"
    )


class ListMonitoringStaff(BaseAPIView):
    serializer_class = MonitoringStaffSerializer
    serializer_class_csv = MonitoringStaffSerializerCSV
    order_by = ["name"]
    queryset = MonitoringStaff.objects.all()


class ListFGD(BaseAPIView):
    serializer_class = FGDSerializer
    serializer_class_csv = FGDSerializerCSV
    filterset_class = FGDFilterSet
    order_by = ["fgyear", "settlement__pk", "fgdid"]
    queryset = FGD.objects.select_related("settlement")


class ListGlobalStep(BaseHouseholdRelatedView):
    perms_lookup_base = "household"
    serializer_class = GlobalStepSerializer
    serializer_class_csv = GlobalStepSerializerCSV
    queryset = GlobalStep.objects.select_related(
        "household__settlement__mpa", "household__settlement"
    )


class ListGlobalThreat(BaseHouseholdRelatedView):
    perms_lookup_base = "household"
    serializer_class = GlobalThreatSerializer
    serializer_class_csv = GlobalThreatSerializerCSV
    queryset = GlobalThreat.objects.select_related(
        "household__settlement__mpa", "household__settlement"
    )


class ListHabitat(BaseFGDView):
    serializer_class = HabitatSerializer
    serializer_class_csv = HabitatSerializerCSV
    queryset = Habitat.objects.select_related("fgd__settlement")


class ListHabitatRule(BaseKIIView):
    serializer_class = HabitatRuleSerializer
    serializer_class_csv = HabitatRuleSerializerCSV
    queryset = HabitatRule.objects.select_related("kii__mpa", "kii__settlement")


class ListHousehold(BaseHouseholdView):
    serializer_class = HouseholdSerializer
    serializer_class_csv = HouseholdSerializerCSV
    filterset_class = HouseholdKIIFilterSet
    order_by = ["household__yearmonitoring", "settlement__mpa__pk", "settlement__pk", "householdid"]
    queryset = Household.objects.select_related("settlement__mpa", "settlement")


class ListKII(BaseAPIView):
    serializer_class = KIISerializer
    serializer_class_csv = KIISerializerCSV
    filterset_class = HouseholdKIIFilterSet
    order_by = ["household__yearmonitoring", "settlement__mpa__pk", "settlement__pk"]
    queryset = KII.objects.select_related("settlement__mpa", "settlement")


class ListLocalStep(BaseHouseholdRelatedView):
    perms_lookup_base = "household"
    serializer_class = LocalStepSerializer
    serializer_class_csv = LocalStepSerializerCSV
    queryset = LocalStep.objects.select_related(
        "household__settlement__mpa", "household__settlement"
    )


class ListLocalThreat(BaseHouseholdRelatedView):
    perms_lookup_base = "household"
    serializer_class = LocalThreatSerializer
    serializer_class_csv = LocalThreatSerializerCSV
    queryset = LocalThreat.objects.select_related(
        "household__settlement__mpa", "household__settlement"
    )


class ListMarineOrganizationMembership(BaseHouseholdRelatedView):
    perms_lookup_base = "household"
    serializer_class = MarineOrganizationMembershipSerializer
    serializer_class_csv = MarineOrganizationMembershipSerializerCSV
    queryset = MarineOrganizationMembership.objects.select_related(
        "household__settlement__mpa", "household__settlement"
    )


class ListMPA(BaseAPIView):
    serializer_class = MPASerializer
    serializer_class_csv = MPASerializerCSV
    order_by = ["name", "est_year"]
    queryset = MPA.objects.all()


class ListNonMarineOrganizationMembership(BaseHouseholdRelatedView):
    perms_lookup_base = "household"
    serializer_class = NonMarineOrganizationMembershipSerializer
    serializer_class_csv = NonMarineOrganizationMembershipSerializerCSV
    queryset = NonMarineOrganizationMembership.objects.select_related(
        "household__settlement__mpa", "household__settlement"
    )


class ListRight(BaseKIIView):
    serializer_class = RightSerializer
    serializer_class_csv = RightSerializerCSV
    queryset = Right.objects.select_related("kii__mpa", "kii__settlement")


class ListRule(BaseFGDView):
    serializer_class = RuleSerializer
    serializer_class_csv = RuleSerializerCSV
    queryset = Rule.objects.select_related("fgd__settlement")


class ListSettlement(BaseAPIView):
    serializer_class = SettlementSerializer
    serializer_class_csv = SettlementSerializerCSV
    order_by = ["mpa__pk", "name"]
    queryset = Settlement.objects.select_related("mpa")


class ListSpecies(BaseFGDView):
    serializer_class = SpeciesSerializer
    serializer_class_csv = SpeciesSerializerCSV
    queryset = Species.objects.select_related("fgd__settlement")


class ListSpeciesRule(BaseKIIView):
    serializer_class = SpeciesRuleSerializer
    serializer_class_csv = SpeciesRuleSerializerCSV
    queryset = SpeciesRule.objects.select_related("kii__mpa", "kii__settlement")


class ListStakeholder(BaseFGDView):
    serializer_class = StakeholderSerializer
    serializer_class_csv = StakeholderSerializerCSV
    queryset = Stakeholder.objects.select_related("fgd__settlement")


class ListZone(BaseKIIView):
    serializer_class = ZoneSerializer
    serializer_class_csv = ZoneSerializerCSV
    queryset = Zone.objects.select_related("kii__mpa", "kii__settlement")


class LookupsListView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response(
            {
                "MPANetwork": LkpMPANetworkSerializer(
                    MPANetwork.objects.all(), many=True
                ).data,
                "Seascape": LkpSeascapeSerializer(
                    Seascape.objects.all(), many=True
                ).data,
                "LkpAssetAssistance": LkpAssetAssistanceSerializer(
                    LkpAssetAssistance.objects.all(), many=True
                ).data,
                "LkpAssetObtain": LkpAssetObtainSerializer(
                    LkpAssetObtain.objects.all(), many=True
                ).data,
                "LkpFreqFishTime": LkpFreqFishTimeSerializer(
                    LkpFreqFishTime.objects.all(), many=True
                ).data,
                "LkpFishTechCategory": LkpFishTechCategorySerializer(
                    LkpFishTechCategory.objects.all(), many=True
                ).data,
                "LkpFishTechnique": LkpFishTechniqueSerializer(
                    LkpFishTechnique.objects.all(), many=True
                ).data,
                "LkpLivelihood": LkpLivelihoodSerializer(
                    LkpLivelihood.objects.all(), many=True
                ).data,
                "LkpNoneToAllScale": LkpNoneToAllScaleSerializer(
                    LkpNoneToAllScale.objects.all(), many=True
                ).data,
                "HouseholdSurveyVersion": HouseholdSurveyVersionSerializer(
                    HouseholdSurveyVersion.objects.all(), many=True
                ).data,
                "FGDSurveyVersion": FGDSurveyVersionSerializer(
                    FGDSurveyVersion.objects.all(), many=True
                ).data,
                "KIISurveyVersion": KIISurveyVersionSerializer(
                    KIISurveyVersion.objects.all(), many=True
                ).data,
                "SKIP_CODES": [{"id": c[0], "label": c[1]} for c in SKIP_CODES],
                "YEAR_CHOICES": [{"id": c[0], "label": c[1]} for c in YEAR_CHOICES],
                "YES_NO_CHOICES": [{"id": c[0], "label": c[1]} for c in YES_NO_CHOICES],
                "GENDER_CHOICES": [{"id": c[0], "label": c[1]} for c in GENDER_CHOICES],
                "KII_FREQ_CHOICES": [
                    {"id": c[0], "label": c[1]} for c in KII_FREQ_CHOICES
                ],
                "MONITORING_FREQUENCY_CHOICES": [
                    {"id": c[0], "label": c[1]} for c in MONITORING_FREQUENCY_CHOICES
                ],
                "ORGANIZATION_POSITION_CHOICES": [
                    {"id": c[0], "label": c[1]} for c in ORGANIZATION_POSITION_CHOICES
                ],
                "TREATMENT_CHOICES": [
                    {"id": c[0], "label": c[1]} for c in Settlement.TREATMENT_CHOICES
                ],
                "EDUCATION_LEVEL_CHOICES": [
                    {"id": c[0], "label": c[1]}
                    for c in Demographic.EDUCATION_LEVEL_CHOICES
                ],
                "RELATIONSHIP_CHOICES": [
                    {"id": c[0], "label": c[1]}
                    for c in Demographic.RELATIONSHIP_CHOICES
                ],
                "ATT_SCALE_CHOICES": [
                    {"id": c[0], "label": c[1]} for c in Household.ATT_SCALE_CHOICES
                ],
                "COOKING_FUEL_CHOICES": [
                    {"id": c[0], "label": c[1]} for c in Household.COOKING_FUEL_CHOICES
                ],
                "ECONOMIC_STATUS_TREND_CHOICES": [
                    {"id": c[0], "label": c[1]}
                    for c in Household.ECONOMIC_STATUS_TREND_CHOICES
                ],
                "FS_CHOICES": [
                    {"id": c[0], "label": c[1]} for c in Household.FS_CHOICES
                ],
                "FS_FREQ_CHOICES": [
                    {"id": c[0], "label": c[1]} for c in Household.FS_FREQ_CHOICES
                ],
                "RELIGION_CHOICES": [
                    {"id": c[0], "label": c[1]} for c in Household.RELIGION_CHOICES
                ],
                "SOCIAL_CONFLICT_CHOICES": [
                    {"id": c[0], "label": c[1]}
                    for c in Household.SOCIAL_CONFLICT_CHOICES
                ],
                "KII_GOVT_SUPPORT_CHOICES": [
                    {"id": c[0], "label": c[1]} for c in Right.KII_GOVT_SUPPORT_CHOICES
                ],
                "KII_RULE_INCLUDED_CHOICES": [
                    {"id": c[0], "label": c[1]} for c in Right.KII_RULE_INCLUDED_CHOICES
                ],
            }
        )
