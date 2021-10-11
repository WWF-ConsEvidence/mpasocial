from django.core.management.base import BaseCommand, CommandError
import argparse
import sys
from api.ingest.utils import get_table_import

# from api.models import Country
from api.models import MPA
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
from api.models import Demographic
from api.models import Death
from api.models import KII
from api.models import FGD
from api.models import Birth

from api.models import (
    MPA_TABLE,
    SETTLEMENT_TABLE,
    ENUMERATOR_TABLE,
    COUNTRY_TABLE,
    FIELDCOORDINATOR_TABLE,
    LIVELIHOOD_TABLE,
    SURVEYVERSION_TABLE,
    FRESHFISHTIME_TABLE,
    ATTITUDESCALE_TABLE,
    DISEASE_TABLE,
    FOODSCURITY_TABLE,
    FOODSCURITYSKIP_TABLE,
    FREQFISHTIME_TABLE,
    GPSFRACTION_TABLE,
    GPSMS_TABLE,
    GROUP_TABLE,
    LIVELIHOOD_TABLE,
    MAJORFISHTECH_TABLE,
    NONETOALLSCALE_TABLE,
    PROPORTION_TABLE,
    STAKEHOLDER_TABLE,
    SURVEYVERSION_TABLE,
    YESNOGOV_TABLE,
    YESNOHH_TABLE,
    YESNOSKIP_TABLE,
    HOUSEHOLD_TABLE,
    BIRTH_TABLE,
    DEATH_TABLE,
    LOCALSTEP_TABLE,
    DEMOGRAPHIC_TABLE,
    GLOBALSTEP_TABLE,
    GLOBALTHREAT_TABLE,
    LOCALTHREAT_TABLE,
    MORGANIZATION_TABLE,
    NMORGANIZATION_TABLE,
    FISHTECHNIQUE_TABLE,
)


class Command(BaseCommand):
    table_choices = (
        MPA_TABLE,
        SETTLEMENT_TABLE,
        ENUMERATOR_TABLE,
        COUNTRY_TABLE,
        FIELDCOORDINATOR_TABLE,
        LIVELIHOOD_TABLE,
        SURVEYVERSION_TABLE,
        FRESHFISHTIME_TABLE,
        ATTITUDESCALE_TABLE,
        DISEASE_TABLE,
        FOODSCURITY_TABLE,
        FOODSCURITYSKIP_TABLE,
        FREQFISHTIME_TABLE,
        GPSFRACTION_TABLE,
        GPSMS_TABLE,
        GROUP_TABLE,
        LIVELIHOOD_TABLE,
        MAJORFISHTECH_TABLE,
        NONETOALLSCALE_TABLE,
        PROPORTION_TABLE,
        STAKEHOLDER_TABLE,
        SURVEYVERSION_TABLE,
        YESNOGOV_TABLE,
        YESNOHH_TABLE,
        YESNOSKIP_TABLE,
        HOUSEHOLD_TABLE,
        BIRTH_TABLE,
        DEATH_TABLE,
        LOCALSTEP_TABLE,
        GLOBALSTEP_TABLE,
        GLOBALTHREAT_TABLE,
        LOCALTHREAT_TABLE,
        DEMOGRAPHIC_TABLE,
        MORGANIZATION_TABLE,
        NMORGANIZATION_TABLE,
        FISHTECHNIQUE_TABLE,
    )

    def add_arguments(self, parser):
        parser.add_argument("datafile", nargs=1, type=argparse.FileType("r"))
        parser.add_argument("--table", choices=self.table_choices)
        parser.add_argument(
            "--clear-existing",
            action="store_true",
            help="Remove existing collect records for protocol before ingesting file",
        )
        parser.add_argument(
            "--tofile",
            action="store_true",
            help="Remove existing collect records for protocol before ingesting file",
        )

    def handle(self, datafile, table, clear_existing, tofile, *args, **options):
        datafile = datafile[0]

        _importer = get_table_import(table)

        if _importer is None:
            raise NotImplementedError()

        _importer(datafile, table, clear_existing, tofile)

        sys.exit(0)
