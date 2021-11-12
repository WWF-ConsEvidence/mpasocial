from django.core.management.base import BaseCommand, CommandError
import argparse
import sys

# from api.models import Country
from api.models.base import MPA
from api.models.household import *
from api.ingest.utils import get_table_import

class Command(BaseCommand):
    table_choices = (
        "mpa",
        "country",
        "monitoringstaff",
        "household",
        "settlement",
        "lkpassetobtain",
        "lkpfishtechcategory",
        "lkpassetassistance",
        "birth",
        "death",
        "demographic",
        "fgdlkpsurveyversion",
        "fgd",
        "globalstep",
        "globalthreat",
        "habitat",
        "habitatrule",
        "kii",
        "kiisurveyversion",
        "lkpfishtechnique",
        "lkpfreqfishtime",
        "lkplivelihood",
        "lkpnonetoallscale",
        "localstep",
        "localthreat",
        "marineorganizationmembership",
        "nonmarineorganizationmembership",
        "mpainterviewyear",
        "mpanetwork",
        "right",
        "rule",
        "seascape",
        "species",
        "speciesrule",
        "stakeholder",
        "users",
        "zone",
        "fgdsurveyversion",
        "householdsurveyversion",
    )

    def add_arguments(self, parser):
        parser.add_argument("datafile", nargs=1, type=argparse.FileType("r", encoding='utf-8-sig', errors='ignore'))
        parser.add_argument("--table", choices=self.table_choices)
        parser.add_argument(
            "--clear-existing",
            action="store_true",
            help="Remove existing records for protocol before ingesting file",
        )
        parser.add_argument(
            "--tofile",
            action="store_true",
            help="Remove existing records for protocol before ingesting file",
        )

    def handle(self, datafile, table, clear_existing, tofile, *args, **options):
        datafile = datafile[0]

        _importer = get_table_import(table)

        if _importer is None:
            raise NotImplementedError()

        _importer(datafile, table, clear_existing, tofile)

        sys.exit(0)
