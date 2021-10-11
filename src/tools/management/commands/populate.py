from django.core.management.base import BaseCommand

# from api.models import Country
# from api.models import MPA
from api.models import Household
from api.models import Team

# from api.models import Stakeholder
# from api.models import Species
from api.models import Settlement

# from api.models import Rule
# from api.models import MarineOrganizationMembership
# from api.models import NonMarineOrganizationMembership
# from api.models import LocalThreat
# from api.models import LocalStep
# from api.models import YesNoSkip
# from api.models import YesNoGov
# from api.models import YesNoHH
# from api.models import SurveyVersion
# from api.models import Proportion
# from api.models import NoneToAllScale
# from api.models import LongitudeDegree
# from api.models import Livelihood
# from api.models import LatitudeDegree
# from api.models import Group
# from api.models import GpsMinutesSecond
# from api.models import GpsFraction
# from api.models import FoodSecuritySkip
# from api.models import FoodSecurity
# from api.models import FreqFishTime
from api.models import FieldCoordinator

# from api.models import Enumerator
# from api.models import Disease
# from api.models import AttitudeScale
# from api.models import Zone
# from api.models import SpeciesRule
# from api.models import Right
# from api.models import HabitatRule
# from api.models import Habitat
# from api.models import GlobalThreat
# from api.models import GlobalStep
# from api.models import Demographic
# from api.models import Death
from api.models import KII
from api.models import FGD
from api.models import Birth

from autofixture import AutoFixture

FIXTURES = ["attitude_scale.json", "country.json", "disease.json"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        Team.truncate()
        FGD.truncate()
        Household.truncate()
        Settlement.truncate()
        KII.truncate()
        FieldCoordinator.truncate()
        Birth.truncate()

        fixture = AutoFixture(Team)
        fixture.create(100)

        fgdfixture = AutoFixture(FGD)
        fgdfixture.create(100)

        fixture = AutoFixture(Household)
        fixture.create(100)

        fixture = AutoFixture(Settlement)
        fixture.create(100)

        fixture = AutoFixture(KII)
        fixture.create(100)

        fixture = AutoFixture(FieldCoordinator)
        fixture.create(40)

        fixture = AutoFixture(Birth)
        fixture.create(40)
