from django.core.management.base import BaseCommand
from api.models.base import *
from api.models.household import *
from api.models.fgd import *
from api.models.kii import *
from django.db.models.deletion import ProtectedError


class Command(BaseCommand):
    def handle(self, *args, **options):
        # models = [Birth,Death,Demographic,GlobalStep,GlobalThreat,Household,Habitat,Species,Stakeholder,FGD,HabitatRule,Right,SpeciesRule,KII,Settlement,MPAInterviewYear,MPA]
        models = [

            Settlement,
            # MPA,
            MPANetwork,
            MPAInterviewYear,
            KII,
            # LkpAssetObtain,
            # LkpAssetAssistance,
            # HouseholdSurveyVersion,
            Birth,
            Death,
            Demographic,
            Habitat,
            FGD,
            MonitoringStaff,
            FGDSurveyVersion,
            GlobalStep,
            GlobalThreat,
            # KIISurveyVersion,
            LocalStep,
            LocalThreat,
            Household,
            # LkpFishTechCategory,
            # LkpFishTechnique,
            # LkpFreqFishTime,
            # LkpLivelihood,
            # LkpNoneToAllScale,

            MarineOrganizationMembership,
            NonMarineOrganizationMembership,
            HabitatRule,
            Right,
            Rule,
            Seascape,
            Species,
            SpeciesRule,
            Stakeholder,
        ]
        for model in models:
            print("clearing", model.__name__,"...")
            try:
                model.objects.all().delete()
            except ProtectedError as e:
                print(e.args[0])

                
            Settlement,
            MPA,
            MPANetwork,
            MPAInterviewYear,
            KII,
            LkpAssetObtain,
            LkpAssetAssistance,
            HouseholdSurveyVersion,
            Birth,
            Death,
            Demographic,
            Habitat,
            FGD,
            MonitoringStaff,
            FGDSurveyVersion,
            GlobalStep,
            GlobalThreat,
            KIISurveyVersion,
            LocalStep,
            LocalThreat,
            Household,
            LkpFishTechCategory,
            LkpFishTechnique,
            LkpFreqFishTime,
            LkpLivelihood,
            LkpNoneToAllScale,
            MarineOrganizationMembership,
            NonMarineOrganizationMembership,
            HabitatRule,
            Right,
            Rule,
            Seascape,
            Species,
            SpeciesRule,
            Stakeholder,
