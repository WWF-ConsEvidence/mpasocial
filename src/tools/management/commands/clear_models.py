from django.core.management.base import BaseCommand
from api.models.base import *
from api.models.household import *
from api.models.fgd import *
from api.models.kii import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        models = [Birth,Death,Demographic,GlobalStep,GlobalThreat,Household,Habitat,FGD,KII,Settlement,MPA]
        for model in models:
            print(model.__name__)
            model.objects.all().delete()
