import csv
import json
from django.db import connection, transaction, IntegrityError
import datetime
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime

import sys


from api.models import MPA
from api.models import Country
from api.models import Settlement
from api.models import Enumerator
from api.models import FieldCoordinator
from api.models import LkpLivelihood
from api.models import HouseholdSurveyVersion
from api.models import LkpFreqFishTime
from api.models import LkpAttitudeScale
from api.models import LkpDisease
from api.models import LkpFoodSecurity
from api.models import LkpFoodSecuritySkip
from api.models import LkpFreqFishTime
from api.models import LkpGpsFraction
from api.models import LkpGpsMinutesSecond
from api.models import LkpGroup
from api.models import LkpLivelihood
from api.models import LkpMajorFishTechnique
from api.models import LkpNoneToAllScale
from api.models import LkpProportion
from api.models import LkpStakeholder
from api.models import HouseholdSurveyVersion
from api.models import LkpYesNoGov
from api.models import LkpYesNoHH
from api.models import LkpYesNoSkip
from api.models import LkpFishTechnique
from api.models import Household
from api.models import Birth
from api.models import Death
from api.models import LocalStep
from api.models import Demographic
from api.models import GlobalStep
from api.models import GlobalThreat
from api.models import LocalThreat
from api.models import MarineOrganizationMembership
from api.models import NonMarineOrganizationMembership
from api.models import LkpFishTechCategory

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
    GLOBALSTEP_TABLE,
    GLOBALTHREAT_TABLE,
    LOCALTHREAT_TABLE,
    DEMOGRAPHIC_TABLE,
    MORGANIZATION_TABLE,
    NMORGANIZATION_TABLE,
    FISHTECHNIQUE_TABLE,
)

settings.TIME_ZONE


model_choice = {
    "livelihood": {"model": LkpLivelihood, "table": "lkp_livelihood"},
    "surveyversion": {"model": HouseholdSurveyVersion, "table": "lkp_survey_version"},
    "freqfishtime": {"model": LkpFreqFishTime, "table": "lkp_freq_fish_time"},
    "attitudescale": {"model": LkpAttitudeScale, "table": "lkp_attitude_scale"},
    "disease": {"model": LkpDisease, "table": "lkp_disease"},
    "foodsecurity": {"model": LkpFoodSecurity, "table": "lkp_food_security"},
    "foodsecurityskip": {
        "model": LkpFoodSecuritySkip,
        "table": "lkp_food_security_skip",
    },
    "gpsfraction": {"model": LkpGpsFraction, "table": "lkp_gps_fraction"},
    "gpsms": {"model": LkpGpsMinutesSecond, "table": "lkp_gps_minutes_second"},
    "group": {"model": LkpGroup, "table": "lkp_group"},
    "majorfishtech": {
        "model": LkpMajorFishTechnique,
        "table": "lkp_major_fish_technique",
    },
    "nonetoallscale": {"model": LkpNoneToAllScale, "table": "lkp_none_to_all_scale"},
    "proportion": {"model": LkpProportion, "table": "lkp_proportion"},
    "stakeholder": {"model": LkpStakeholder, "table": "lkp_stakeholder"},
    "yesnogov": {"model": LkpYesNoGov, "table": "lkp_yes_no_gov"},
    "yesnohh": {"model": LkpYesNoHH, "table": "lkp_yes_no_hh"},
    "yesnoskip": {"model": LkpYesNoSkip, "table": "lkp_yes_no_skip"},
    "household": {"model": Household, "table": "household"},
    "country": {"model": Country, "table": "country"},
    "mpa": {"model": MPA, "table": "mpa"},
    "fieldcoordinator": {"model": FieldCoordinator, "table": "field_coordinator"},
    "enumerator": {"model": Enumerator, "table": "enumerator"},
    "birth": {"model": Birth, "table": "birth"},
    "death": {"model": Death, "table": "death"},
    "localstep": {"model": LocalStep, "table": "local_step"},
    "globalstep": {"model": GlobalStep, "table": "global_step"},
    "globalthreat": {"model": GlobalThreat, "table": "global_threat"},
    "localthreat": {"model": LocalThreat, "table": "local_threat"},
    "demographic": {"model": Demographic, "table": "demographic"},
    "morganization": {
        "model": MarineOrganizationMembership,
        "table": "marine_organization_membership",
    },
    "nmorganization": {
        "model": NonMarineOrganizationMembership,
        "table": "non_marine_organization_membership",
    },
    "fishtechnique": {"model": LkpFishTechnique, "table": "lkp_fish_technique"},
}


def get_ingest_project_choices():
    project_choices = dict()
    project_choices["data__mpa"] = {str(s.mpaid): s for s in MPA.objects.all()}

    project_choices["data__settlement"] = {
        str(s.settlementid): s for s in Settlement.objects.all()
    }
    project_choices["data__countries"] = {str(s.id): s for s in Country.objects.all()}
    project_choices["data__enumerator"] = {
        str(s.pk): s for s in Enumerator.objects.all()
    }

    project_choices["data__fieldcoordinator"] = {
        str(s.pk): s for s in FieldCoordinator.objects.all()
    }
    project_choices["data__surveyversion"] = {
        str(s.pk): s for s in HouseholdSurveyVersion.objects.all()
    }
    project_choices["data__livelihood"] = {
        str(s.code): s for s in LkpLivelihood.objects.all()
    }
    project_choices["data__freqfishtime"] = {
        str(s.code): s for s in LkpFreqFishTime.objects.all()
    }
    project_choices["data__nonetoallscale"] = {
        str(s.code): s for s in LkpNoneToAllScale.objects.all()
    }
    project_choices["data__foodsecurity"] = {
        str(s.code): s for s in LkpFoodSecurity.objects.all()
    }
    project_choices["data__majorfishtech"] = {
        str(s.code): s for s in LkpMajorFishTechnique.objects.all()
    }
    project_choices["data__household"] = {str(s.pk): s for s in Household.objects.all()}
    project_choices["data__fishtechcategory"] = {
        str(s.pk): s for s in LkpFishTechCategory.objects.all()
    }

    return project_choices


def import_mpa(datafile, identifier, cleardata, tofile):
    print("importing " + identifier)
    thechoices = get_ingest_project_choices()
    if cleardata:
        MPA.objects.all().delete()
    reader = csv.DictReader(datafile)
    lookuperrors = []
    for row in reader:
        if row["country"]:
            try:
                country = thechoices["data__countries"][row["country"]]
            except (KeyError):
                lookuperrors.append([row["mpaid"], row["country"], "country"])
                continue
            row["country"] = country
        else:
            row["country"] = None

    datafile.seek(0)
    reader = csv.DictReader(datafile)

    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)

    for row in reader:
        if row["country"]:
            country = thechoices["data__countries"][row["country"]]
            row["country"] = country
        try:
            MPA.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["mpaid"]))
            sys.exit()
    print("Import complete.")


def import_settlement(datafile, identifier, cleardata, tofile):
    print("importing " + identifier)
    if cleardata:
        Settlement.objects.all().delete()
    reader = csv.DictReader(datafile)
    thechoices = get_ingest_project_choices()
    lookuperrors = []
    for row in reader:
        try:
            mpa = thechoices["data__mpa"][row["mpa"]]
        except (KeyError):
            lookuperrors.append([row["settlementid"], row["mpa"], "mpa"])
            continue

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        mpa = thechoices["data__mpa"][row["mpa"]]
        row["mpa"] = mpa
        try:
            if row["districtcode"] == "":
                row["districtcode"] = None
            Settlement.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["settlementid"]))
            sys.exit()
    print("Import complete.")


def import_birth(datafile, identifier, cleardata, tofile):
    print("importing " + identifier)
    if cleardata:
        Birth.objects.all().delete()
    reader = csv.DictReader(datafile)
    thechoices = get_ingest_project_choices()
    lookuperrors = []
    for row in reader:
        try:
            household = thechoices["data__household"][row["household"]]
        except (KeyError):
            lookuperrors.append([row["birthid"], row["household"], "household"])
            continue

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        if row["dateofdeath"] == "":
            row["dateofdeath"] = None
        if row["infantsurvived"] == "":
            row["infantsurvived"] = None
        household = thechoices["data__household"][row["household"]]
        row["household"] = household
        try:
            Birth.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["birthid"]))
            sys.exit()
    print("Import complete.")


def import_death(datafile, identifier, cleardata, tofile):
    print("importing " + identifier)
    if cleardata:
        Death.objects.all().delete()
    reader = csv.DictReader(datafile)
    thechoices = get_ingest_project_choices()
    lookuperrors = []

    for row in reader:
        try:
            household = thechoices["data__household"][row["household"]]
        except (KeyError):
            lookuperrors.append([row["birthid"], row["household"], "household"])
            continue

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        if row["dateofdeath"] == "":
            row["dateofdeath"] = None
        if row["ageatdeath"] == "":
            row["ageatdeath"] = None
        household = thechoices["data__household"][row["household"]]
        row["household"] = household
        newrow = {k: (v if v else None) for k, v in row.items()}
        try:
            Death.objects.create(**newrow)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["deathid"]))
            sys.exit()
    print("Import complete.")


def import_enumerator(datafile, identifier, cleardata, tofile):
    print("importing " + identifier)
    if cleardata:
        Enumerator.objects.all().delete()
    reader = csv.DictReader(datafile)
    for row in reader:
        try:
            Enumerator.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["code"]))
            sys.exit()
    print("Import complete.")


def import_country(datafile, identifier, cleardata, tofile):
    print("importing country")
    if cleardata:
        Country.objects.all().delete()
    reset_pk("country_id_seq", 1, identifier)
    reader = csv.DictReader(datafile)
    for row in reader:
        try:
            Country.objects.create(**row)
        except (IntegrityError):
            print("Duplicate primary key. Import failed. Clear existing data.")
            sys.exit()
    print("Import complete.")


def import_fieldcoordinator(datafile, identifier, cleardata, tofile):
    print("importing field coordinators")
    if cleardata:
        FieldCoordinator.objects.all().delete()
    reader = csv.DictReader(datafile)
    for row in reader:
        try:
            FieldCoordinator.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["coordinatorcode"]))
            sys.exit()
    print("Import complete.")


def import_fishtechnique(datafile, identifier, cleardata):
    print("importing fish technique")

    if cleardata:
        LkpFishTechnique.objects.all().delete()
    reader = csv.DictReader(datafile)
    thechoices = get_ingest_project_choices()

    lookuperrors = []

    for row in reader:
        try:
            fishtechcategory = thechoices["data__fishtechcategory"][
                row["consolidatedfishtechcategory"]
            ]
        except (KeyError):
            lookuperrors.append(
                [
                    row["code"],
                    row["consolidatedfishtechcategory"],
                    "consolidatedfishtechcategory",
                ]
            )
            continue

        row["consolidatedfishtechcategory"] = fishtechcategory

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        try:
            fishtechcategory = thechoices["data__fishtechcategory"][
                row["consolidatedfishtechcategory"]
            ]
        except (KeyError):
            print(
                "consolidatedfishtechcategory "
                + row["consolidatedfishtechcategory"]
                + " could not be found. Import failed"
            )
        row["consolidatedfishtechcategory"] = fishtechcategory
        try:
            LkpFishTechnique.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["code"]))
            sys.exit()
    print("Import complete.")


def import_demographic(datafile, identifier, cleardata, tofile):
    print("importing " + identifier)

    thechoices = get_ingest_project_choices()
    reader = csv.DictReader(datafile)
    # disable temporarily
    # print("Skipping demo for performance")
    # return
    if cleardata:
        Demographic.objects.all().delete()

    lookuperrors = []
    for row in reader:
        try:
            household = thechoices["data__household"][row["household"]]
        except (KeyError):
            lookuperrors.append([row["demographicid"], row["household"], "household"])
            continue

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        print(row["demographicid"])
        if int(row["demographicid"]) < 0:
            continue
        for fld in [
            "individualedlevel",
            "individualdaysunwell",
            "individuallostdays",
            "individualunwell",
            "individualenrolled",
            "individualage",
            "individualgender",
            "relationhhh",
            "householdhead",
        ]:
            row[fld] = None if not row[fld] else row[fld]

        household = thechoices["data__household"][row["household"]]
        row["household"] = household
        try:
            Demographic.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["demographicid"]))
            sys.exit()
    print("Import complete.")


def import_globalstep(datafile, identifier, cleardata, tofile):
    print("importing global step")
    if cleardata:
        GlobalStep.objects.all().delete()
    thechoices = get_ingest_project_choices()
    reader = csv.DictReader(datafile)

    lookuperrors = []
    for row in reader:
        try:
            household = thechoices["data__household"][row["household"]]
        except (KeyError):
            lookuperrors.append([row["globalstepsid"], row["household"], "household"])
            continue

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        household = thechoices["data__household"][row["household"]]
        if row["entryhouseholdid"] == "":
            row["entryhouseholdid"] = None
        row["household"] = household
        try:
            GlobalStep.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["globalstepsid"]))
            sys.exit()
    print("Import complete.")


def import_localstep(datafile, identifier, cleardata, tofile):
    print("importing local step")
    if cleardata:
        LocalStep.objects.all().delete()
    thechoices = get_ingest_project_choices()
    reader = csv.DictReader(datafile)
    lookuperrors = []
    for row in reader:
        try:
            household = thechoices["data__household"][row["household"]]
        except (KeyError):
            lookuperrors.append([row["localstepsid"], row["household"], "household"])
            continue

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        household = thechoices["data__household"][row["household"]]
        if row["entryhouseholdid"] == "":
            row["entryhouseholdid"] = None
        row["household"] = household
        try:
            LocalStep.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["localstepsid"]))
            sys.exit()
    print("Import complete.")


def import_globalthreat(datafile, identifier, cleardata, tofile):
    print("importing global threat")
    if cleardata:
        GlobalThreat.objects.all().delete()
    thechoices = get_ingest_project_choices()
    reader = csv.DictReader(datafile)

    lookuperrors = []
    for row in reader:
        try:
            household = thechoices["data__household"][row["household"]]
        except (KeyError):
            lookuperrors.append([row["globalthreatid"], row["household"], "household"])
            continue

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        household = thechoices["data__household"][row["household"]]
        if row["entryhouseholdid"] == "":
            row["entryhouseholdid"] = None
        row["household"] = household
        try:
            GlobalThreat.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["globalthreatid"]))
            sys.exit()
    print("Import complete.")


def import_localthreat(datafile, identifier, cleardata, tofile):
    print("importing local threat")
    if cleardata:
        LocalThreat.objects.all().delete()
    thechoices = get_ingest_project_choices()
    reader = csv.DictReader(datafile)

    lookuperrors = []
    for row in reader:
        try:
            household = thechoices["data__household"][row["household"]]
        except (KeyError):
            lookuperrors.append([row["localthreatid"], row["household"], "household"])
            continue

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        household = (
            thechoices["data__household"][row["household"]]
            if row["household"]
            else None
        )
        if row["entryhouseholdid"] == "":
            row["entryhouseholdid"] = None
        row["household"] = household
        try:
            LocalThreat.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["localthreatid"]))
            sys.exit()
    print("Import complete.")


def import_morganization(datafile, identifier, cleardata, tofile):
    print("importing Marine Organization Membership")
    if cleardata:
        MarineOrganizationMembership.objects.all().delete()
    thechoices = get_ingest_project_choices()
    reader = csv.DictReader(datafile)

    lookuperrors = []
    for row in reader:
        try:
            if row["household"]:
                household = thechoices["data__household"][row["household"]]
        except (KeyError):
            lookuperrors.append([row["morganizationid"], row["household"], "household"])
            continue

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        household = (
            thechoices["data__household"][row["household"]]
            if row["household"]
            else None
        )
        if row["entryhouseholdid"] == "":
            row["entryhouseholdid"] = None
        for fld in ["entryhouseholdid", "position", "meeting", "days", "contribution"]:
            row[fld] = None if not row[fld] else row[fld]
        row["household"] = household
        try:
            MarineOrganizationMembership.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["morganizationid"]))
            sys.exit()
    print("Import complete.")


def import_nmorganization(datafile, identifier, cleardata, tofile):
    print("importing Non Marine Organization Membership")
    if cleardata:
        NonMarineOrganizationMembership.objects.all().delete()
    thechoices = get_ingest_project_choices()
    reader = csv.DictReader(datafile)

    lookuperrors = []
    for row in reader:
        try:
            if row["household"]:
                household = thechoices["data__household"][row["household"]]
        except (KeyError):
            lookuperrors.append(
                [row["nmorganizationid"], row["household"], "household"]
            )
            continue

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        household = (
            thechoices["data__household"][row["household"]]
            if row["household"]
            else None
        )
        if row["entryhouseholdid"] == "":
            row["entryhouseholdid"] = None
        for fld in ["entryhouseholdid", "position", "meeting", "days", "contribution"]:
            row[fld] = None if not row[fld] else row[fld]
        row["household"] = household
        try:
            NonMarineOrganizationMembership.objects.create(**row)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["nmorganizationid"]))
            sys.exit()
    print("Import complete.")


def import_lookup(datafile, identifier, cleardata, tofile):
    print("importing lookup:" + identifier)
    themodel = model_choice[identifier]["model"]
    if cleardata:
        themodel.objects.all().delete()
    reader = csv.DictReader(datafile)
    for row in reader:
        try:
            themodel.objects.create(**row)
        except (IntegrityError):
            print("Duplicate primary. Import failed.")
            sys.exit()
    print("Import complete.")


def import_household(datafile, identifier, cleardata, tofile):
    print("importing household")
    if cleardata:
        Household.objects.all().delete()
    reader = csv.DictReader(datafile)
    mpatruth = {
        "TRUE": True,
        "FALSE": False,
        "true": True,
        "false": False,
        "NONE": None,
        "1": True,
        "0": False,
        1: True,
        0: False,
    }
    thechoices = get_ingest_project_choices()

    ## check for matching lookups

    lookuperrors = []
    lookupfields = [
        # ["mpa", "mpa"],
        ["settlement", "settlement"],
        ["primaryinterviewer", "enumerator"],
        ["secondaryinterviewer", "enumerator"],
        ["fieldcoordinator", "fieldcoordinator"],
        ["surveyversionnumber", "surveyversion"],
        ["primarylivelihood", "livelihood"],
        ["secondarylivelihood", "livelihood"],
        ["tertiarylivelihood", "livelihood"],
        ["freqfishtime", "freqfishtime"],
        ["freqeatfish", "freqfishtime"],
        ["freqsalefish", "freqfishtime"],
        ["percentproteinfish", "nonetoallscale"],
        ["fsnotenough", "foodsecurity"],
        ["fsdidnotlast", "foodsecurity"],
        ["fsbalanceddiet", "foodsecurity"],
        ["dataentryid", "enumerator"],
        ["datacheckid", "enumerator"],
        ["majorfishtechnique", "majorfishtech"],
    ]
    # print (thechoices["data__enumerator"])
    # return
    for row in reader:
        for thefld in lookupfields:
            try:
                lookupvalue = (
                    thechoices["data__" + thefld[1]][str(row[thefld[0]])]
                    if row[str(thefld[0])]
                    else None
                )
            except (KeyError):
                lookuperrors.append([row["householdid"], row[thefld[0]], thefld[0]])
                continue
    print("check complete")

    datafile.seek(0)
    reader = csv.DictReader(datafile)
    if tofile:
        now = datetime.now()
        current_time = now.strftime("%H_%M_%S")
        f = open("household_" + current_time + ".txt", "a")

    if len(lookuperrors):
        display_errors(lookuperrors, tofile, identifier)
    for row in reader:
        print(row["householdid"])

        for thefld in lookupfields:
            row[thefld[0]] = (
                thechoices["data__" + thefld[1]][row[thefld[0]]]
                if row[thefld[0]]
                else None
            )

        row["dataentrycomplete"] = mpatruth[row["dataentrycomplete"]]
        row["datacheckcomplete"] = mpatruth[row["datacheckcomplete"]]

        # replace blank values with None
        newrow = {k: (v if (v and v != " ") else None) for k, v in row.items()}

        # these two fields cannot be blank
        if newrow["lonfrac"] == None:
            newrow["lonfrac"] = 0
        if newrow["latfrac"] == None:
            newrow["latfrac"] = 0
        try:
            Household.objects.create(**newrow)
        except (IntegrityError):
            print("Duplicate key: {}. Import failed.".format(row["householdid"]))
            sys.exit()
    print("Import complete.")


def get_table_import(table):
    if table == MPA_TABLE:
        return import_mpa
    elif table == SETTLEMENT_TABLE:
        return import_settlement
    elif table == ENUMERATOR_TABLE:
        return import_enumerator
    elif table == COUNTRY_TABLE:
        return import_country
    elif table == FIELDCOORDINATOR_TABLE:
        return import_fieldcoordinator
    elif table == LIVELIHOOD_TABLE:
        return import_lookup
    elif table == SURVEYVERSION_TABLE:
        return import_lookup
    elif table == HOUSEHOLD_TABLE:
        return import_household
    elif table == BIRTH_TABLE:
        return import_birth
    elif table == DEATH_TABLE:
        return import_death
    elif table == DEMOGRAPHIC_TABLE:
        return import_demographic
    elif table == GLOBALSTEP_TABLE:
        return import_globalstep
    elif table == LOCALSTEP_TABLE:
        return import_localstep
    elif table == GLOBALTHREAT_TABLE:
        return import_globalthreat
    elif table == MORGANIZATION_TABLE:
        return import_morganization
    elif table == NMORGANIZATION_TABLE:
        return import_nmorganization
    elif table == FISHTECHNIQUE_TABLE:
        return import_fishtechnique
    elif table == LOCALTHREAT_TABLE:
        return import_localthreat
    elif (
        table == FRESHFISHTIME_TABLE
        or table == FRESHFISHTIME_TABLE
        or table == ATTITUDESCALE_TABLE
        or table == DISEASE_TABLE
        or table == FOODSCURITY_TABLE
        or table == FOODSCURITYSKIP_TABLE
        or table == FREQFISHTIME_TABLE
        or table == GPSFRACTION_TABLE
        or table == GPSMS_TABLE
        or table == GROUP_TABLE
        or table == LIVELIHOOD_TABLE
        or table == MAJORFISHTECH_TABLE
        or table == NONETOALLSCALE_TABLE
        or table == PROPORTION_TABLE
        or table == STAKEHOLDER_TABLE
        or table == SURVEYVERSION_TABLE
        or table == YESNOGOV_TABLE
        or table == YESNOHH_TABLE
        or table == YESNOSKIP_TABLE
    ):
        return import_lookup
    return None


def reset_pk(seq, start, identifier):
    themodel = model_choice[identifier]["model"]
    sql = """
        ALTER SEQUENCE {thesequence} RESTART WITH {start}
        """.format(
        table_name=themodel.objects.model._meta.db_table, thesequence=seq, start=start
    )
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.rowcount


def display_errors(lookuperrors, tofile, identifier):
    if tofile:
        now = datetime.now()
        current_time = now.strftime("%H_%M_%S")
        f = open("importerrors/" + identifier + "_" + current_time + ".txt", "a")
    for error in lookuperrors:
        message = "Row: {}: keyerror: cannot find {} {} in the lookup table".format(
            error[0], error[2], error[1]
        )
        if tofile:
            f.write(message + "\n")

        else:
            print(message)
    if tofile:
        f.close()
        print(
            "Import failed, errors printed to "
            + identifier
            + "_"
            + current_time
            + ".txt"
        )
    sys.exit()
