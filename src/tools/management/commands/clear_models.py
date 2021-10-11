from django.core.management.base import BaseCommand
from api.models import Country
from api.models import MPA
from api.models import Household
from api.models import Team
from api.models import Stakeholder
from api.models import Species
from api.models import Settlement
from api.models import Rule
from api.models import MarineOrganizationMembership
from api.models import NonMarineOrganizationMembership
from api.models import LocalThreat
from api.models import LocalStep
from api.models import LkpYesNoSkip
from api.models import LkpYesNoGov
from api.models import LkpYesNoHH
from api.models import HouseholdSurveyVersion
from api.models import LkpProportion
from api.models import LkpNoneToAllScale
from api.models import LkpLivelihood
from api.models import LkpGroup
from api.models import LkpGpsMinutesSecond
from api.models import LkpGpsFraction
from api.models import LkpFoodSecuritySkip
from api.models import LkpFoodSecurity
from api.models import LkpFreqFishTime
from api.models import FieldCoordinator
from api.models import Enumerator
from api.models import LkpDisease
from api.models import LkpAttitudeScale
from api.models import Zone
from api.models import SpeciesRule
from api.models import Right
from api.models import HabitatRule
from api.models import Habitat
from api.models import GlobalThreat
from api.models import GlobalStep
from api.models import Demographic
from api.models import Death
from api.models import KII
from api.models import FGD
from api.models import Birth


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Country.objects.all().delete()
        MPA.objects.all().delete()
        Household.objects.all().delete()
        Team.objects.all().delete()
        Stakeholder.objects.all().delete()
        Species.objects.all().delete()
        Settlement.objects.all().delete()
        Rule.objects.all().delete()
        MarineOrganizationMembership.objects.all().delete()
        NonMarineOrganizationMembership.objects.all().delete()
        LocalThreat.objects.all().delete()
        LocalStep.objects.all().delete()
        LkpYesNoSkip.objects.all().delete()
        LkpYesNoGov.objects.all().delete()
        LkpYesNoHH.objects.all().delete()
        HouseholdSurveyVersion.objects.all().delete()
        LkpProportion.objects.all().delete()
        LkpNoneToAllScale.objects.all().delete()
        LkpLivelihood.objects.all().delete()
        LkpGroup.objects.all().delete()
        LkpGpsMinutesSecond.objects.all().delete()
        LkpGpsFraction.objects.all().delete()
        LkpFoodSecuritySkip.objects.all().delete()
        LkpFoodSecurity.objects.all().delete()
        LkpFreqFishTime.objects.all().delete()
        FieldCoordinator.objects.all().delete()
        Enumerator.objects.all().delete()
        LkpDisease.objects.all().delete()
        LkpAttitudeScale.objects.all().delete()
        Zone.objects.all().delete()
        SpeciesRule.objects.all().delete()
        Right.objects.all().delete()
        HabitatRule.objects.all().delete()
        Habitat.objects.all().delete()
        GlobalThreat.objects.all().delete()
        GlobalStep.objects.all().delete()
        Demographic.objects.all().delete()
        Death.objects.all().delete()
        KII.objects.all().delete()
        FGD.objects.all().delete()
        Birth.objects.all().delete()
