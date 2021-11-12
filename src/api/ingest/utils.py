import csv
import json
from django.db import connection, transaction, IntegrityError
import datetime
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime
import sys
from api.models.base import *
from api.models.household import *
from api.models.fgd import *
from api.models.kii import *
settings.TIME_ZONE


model_choice = {
    "livelihood": {"model": LkpLivelihood, "table": "lkp_livelihood"},
    "surveyversion": {"model": HouseholdSurveyVersion, "table": "lkp_survey_version"},
    "freqfishtime": {"model": LkpFreqFishTime, "table": "lkp_freq_fish_time"},
    "lkpassetobtain": {"model": LkpAssetObtain, "table": "api_lkpassetobtain"},
    "lkpfishtechcategory": {"model": LkpFishTechCategory, "table": "api_lkpfishtechcategory"},
    "lkpassetassistance": {"model": LkpAssetAssistance, "table": "api_lkpassetassistance"},
    "country": {"model": Country, "table": "country"},
    "death": {"model": Death, "table": "api_death"},
    "birth": {"model": Birth, "table": "api_birth"},
    "settlement": {"model": Settlement, "table": "api_settlement"},
    "fgdlkpsurveyversion": {"model": FGDSurveyVersion, "table": "api_fgdlkpsurveyversion"},
    "fgd": {"model": FGD, "table": "api_fgd"},
    "household": {"model": Household, "table": "api_household"},
    "globalstep": {"model": GlobalStep, "table": "api_globalstep"},
    "globalthreat": {"model": GlobalThreat, "table": "api_globalthreat"},
    "habitat": {"model": Habitat, "table": "api_habitat"},
    "habitatrule": {"model": HabitatRule, "table": "api_habitatrule"},
    "kii": {"model": KII, "table": "api_kii"},
    "kiisurveyversion": {"model": KIISurveyVersion, "table": "api_kiisurveyversion"},
    "lkpfreqfishtime": {"model": LkpFreqFishTime, "table": "api_lkpfreqfishtime"},
    "lkplivelihood": {"model": LkpLivelihood, "table": "api_lkplivelihood"},
    "lkpnonetoallscale": {"model": LkpNoneToAllScale, "table": "api_lkpnonetoallscale"},
    "localstep": {"model": LocalStep, "table": "api_localstep"},
    "localthreat": {"model": LocalThreat, "table": "api_localthreat"},
    "marineorganizationmembership": {"model": MarineOrganizationMembership, "table": "api_marineorganizationmembership"},
    "nonmarineorganizationmembership": {"model": NonMarineOrganizationMembership, "table": "api_nonmarineorganizationmembership"},
    "mpainterviewyear": {"model": MPAInterviewYear, "table": "api_mpainterviewyear"},
    "mpanetwork": {"model": MPANetwork, "table": "api_mpanetwork"},
    "right": {"model": Right, "table": "api_right"},
    "rule": {"model": Rule, "table": "api_rule"},
    "seascape": {"model": Seascape, "table": "api_seascape"},
    "species": {"model": Species, "table": "api_species"},
    "speciesrule": {"model": SpeciesRule, "table": "api_speciesrule"},
    "stakeholder": {"model": Stakeholder, "table": "api_stakeholder"},
    "users": {"model": Users, "table": "api_users"},
    "zone": {"model": Zone, "table": "api_zone"},
    "mpa": {"model": MPA, "table": "api_mpa"},
    "monitoringstaff": {"model": MonitoringStaff, "table": "api_monitoringstaff"},
    "demographic": {"model": Demographic, "table": "api_demographic"},
    "fgdsurveyversion": {"model": FGDSurveyVersion, "table": "api_fgdsurveyversion"},
    "householdsurveyversion": {"model": HouseholdSurveyVersion, "table": "api_householdsurveyversion"},
}


def get_ingest_project_choices():
    # TOD - find a better way to
    project_choices = dict()
    project_choices["data__mpa"] = {str(s.mpaid): s for s in MPA.objects.all()}
    project_choices["data__settlement"] = {str(s.settlementid): s for s in Settlement.objects.all()}
    project_choices["data__country"] = {str(s.pk): s for s in Country.objects.all()}
    project_choices["data__seascape"] = {str(s.pk): s for s in Seascape.objects.all()}
    project_choices["data__mpanetwork"] = {str(s.pk): s for s in MPANetwork.objects.all()}
    monitoringstaff = {str(s.pk): s for s in MonitoringStaff.objects.all()}
    project_choices["data__monitoringstaff"] = monitoringstaff
    project_choices["data__facilitator"] = monitoringstaff
    project_choices["data__notetaker"] = monitoringstaff
    project_choices["data__dataentryid"] = monitoringstaff
    project_choices["data__datacheckid"] = monitoringstaff
    project_choices["data__datacheck"] = monitoringstaff
    project_choices["data__primaryinterviewer"] = monitoringstaff
    project_choices["data__fieldcoordinator"] = monitoringstaff
    project_choices["data__secondaryinterviewer"] = monitoringstaff
    project_choices["data__householdsurveyversion"] = {str(s.pk): s for s in HouseholdSurveyVersion.objects.all()}
    project_choices["data__surveyversionnumber"] = {str(s.pk): s for s in HouseholdSurveyVersion.objects.all()}
    project_choices["data__livelihood"] = {str(s.code): s for s in LkpLivelihood.objects.all()}
    project_choices["data__primarylivelihood"] = {str(s.code): s for s in LkpLivelihood.objects.all()}
    project_choices["data__secondarylivelihood"] = {str(s.code): s for s in LkpLivelihood.objects.all()}
    project_choices["data__tertiarylivelihood"] = {str(s.code): s for s in LkpLivelihood.objects.all()}
    project_choices["data__freqfishtime"] = {str(s.code): s for s in LkpFreqFishTime.objects.all() }
    project_choices["data__freqsalefish"] = {str(s.code): s for s in LkpFreqFishTime.objects.all() }
    project_choices["data__freqeatfish"] = {str(s.code): s for s in LkpFreqFishTime.objects.all() }
    nonetoallscale = {str(s.code): s for s in LkpNoneToAllScale.objects.all()}
    project_choices["data__nonetoallscale"] = nonetoallscale
    project_choices["data__percentincomefish"] = nonetoallscale
    project_choices["data__percentproteinfish"] = nonetoallscale
    project_choices["data__fishtechcategory"] = {str(s.pk): s for s in LkpFishTechCategory.objects.all()}
    project_choices["data__majorfishtechnique"] = {str(s.pk): s for s in LkpFishTechCategory.objects.all()}
    project_choices["data__fishtechnique"] = {str(s.pk): s for s in LkpFishTechnique.objects.all()}
    project_choices["data__primaryfishtechnique"] = {str(s.pk): s for s in LkpFishTechnique.objects.all()}
    project_choices["data__secondaryfishtechnique"] = {str(s.pk): s for s in LkpFishTechnique.objects.all()}
    project_choices["data__tertiaryfishtechnique"] = {str(s.pk): s for s in LkpFishTechnique.objects.all()}
    project_choices["data__assetobtain"] = {str(s.pk): s for s in LkpAssetObtain.objects.all()}
    project_choices["data__assetcarobtain"] = {str(s.pk): s for s in LkpAssetObtain.objects.all()}
    project_choices["data__assetmotorcycleobtain"] = {str(s.pk): s for s in LkpAssetObtain.objects.all()}
    project_choices["data__household"] = {str(s.pk): s for s in Household.objects.all()}
    project_choices["data__fgdversion"] = {str(s.pk): s for s in FGDSurveyVersion.objects.all()}
    assetassistance = {str(s.pk): s for s in LkpAssetAssistance.objects.all()}
    project_choices["data__assetassistance"] = assetassistance
    project_choices["data__assetcarassistance"] = assetassistance
    project_choices['data__assettruckassistance'] = assetassistance
    project_choices['data__assetbicycleassistance'] = assetassistance
    project_choices['data__assetmotorcycleassistance'] = assetassistance
    project_choices['data__assetboatnomotorassistance'] = assetassistance
    project_choices['data__assetboatoutboardassistance'] = assetassistance
    project_choices['data__assetboatinboardassistance'] = assetassistance
    project_choices['data__assetlandlinephoneassistance'] = assetassistance
    project_choices['data__assetcellphoneassistance'] = assetassistance
    project_choices['data__assettvassistance'] = assetassistance
    project_choices['data__assetradioassistance'] = assetassistance
    project_choices['data__assetstereoassistance'] = assetassistance
    project_choices['data__assetcdassistance'] = assetassistance
    project_choices['data__assetdvdassistance'] = assetassistance
    project_choices['data__assetsatelliteassistance'] = assetassistance
    project_choices['data__assetgeneratorassistance'] = assetassistance
    assetobtain = {str(s.pk): s for s in LkpAssetObtain.objects.all()}
    project_choices['data__assetcarobtain'] = assetobtain
    project_choices['data__assettruckobtain'] = assetobtain
    project_choices['data__assetbicycleobtain'] = assetobtain
    project_choices['data__assetmotorcycleobtain'] = assetobtain
    project_choices['data__assetboatnomotorobtain'] = assetobtain
    project_choices['data__assetboatoutboardobtain'] = assetobtain
    project_choices['data__assetboatinboardobtain'] = assetobtain
    project_choices['data__assetlandlinephoneobtain'] = assetobtain
    project_choices['data__assetcellphoneobtain'] = assetobtain
    project_choices['data__assettvobtain'] = assetobtain
    project_choices['data__assetradioobtain'] = assetobtain
    project_choices['data__assetstereoobtain'] = assetobtain
    project_choices['data__assetcdobtain'] = assetobtain
    project_choices['data__assetdvdobtain'] = assetobtain
    project_choices['data__assetsatelliteobtain'] = assetobtain
    project_choices['data__assetgeneratorobtain'] = assetobtain
    project_choices['data__fgd'] = {str(s.pk): s for s in FGD.objects.all()}
    project_choices['data__kiiversion'] = {str(s.pk): s for s in KIISurveyVersion.objects.all()}
    project_choices['data__kii'] = {str(s.pk): s for s in KII.objects.all()}
    project_choices['data__lkpfishtechnique'] = {str(s.pk): s for s in LkpFishTechnique.objects.all()}
    project_choices['data__lkpnonetoallscale'] = {str(s.pk): s for s in LkpNoneToAllScale.objects.all()}
    project_choices['data__userextbnd'] = {str(s.pk): s for s in LkpNoneToAllScale.objects.all()}
    project_choices['data__userintbnd'] = {str(s.pk): s for s in LkpNoneToAllScale.objects.all()}

    return project_choices

related_records = {
    "mpa": ["country","seascape","mpanetwork"],
    "country": [],
    "death": ["household"],
    "birth": ["household"],
    "settlement": ["mpa"],
    "fgdlkpsurveyversion": [],
    "fgd": ["settlement","facilitator","notetaker","fgdversion","dataentryid","datacheckid"],
    "household": ["settlement","primaryinterviewer","secondaryinterviewer","fieldcoordinator",
                  "surveyversionnumber","primarylivelihood","secondarylivelihood","tertiarylivelihood",
                  "freqfishtime","freqsalefish","percentincomefish","freqeatfish","percentproteinfish",
                  "majorfishtechnique","primaryfishtechnique","secondaryfishtechnique","tertiaryfishtechnique",
                  "assetcarobtain","assetcarassistance","assettruckassistance",
                  "assetbicycleassistance","assetmotorcycleassistance","assetboatnomotorassistance",
                  "assetboatoutboardassistance","assetboatinboardassistance","assetlandlinephoneassistance",
                  "assetcellphoneassistance","assettvassistance","assetradioassistance","assetstereoassistance",
                  "assetcdassistance","assetdvdassistance","assetsatelliteassistance","assetgeneratorassistance",
                  "assettruckobtain","assetbicycleobtain","assetmotorcycleobtain",
                  "assetboatnomotorobtain","assetboatoutboardobtain","assetboatinboardobtain",
                  "assetlandlinephoneobtain","assetcellphoneobtain","assettvobtain","assetradioobtain",
                  "assetstereoobtain","assetcdobtain","assetdvdobtain","assetsatelliteobtain",
                  "assetgeneratorobtain","dataentryid"],
    "globalstep": ["household"],
    "globalthreat": ["household"],
    "habitat": ['fgd'],
    "habitatrule": ['kii'],
    "kiisurveyversion": [],
    "lkpfreqfishtime": [],
    "lkplivelihood": [],
    "lkpnonetoallscale": [],
    "kii": ["settlement","fgd","primaryinterviewer","secondaryinterviewer","kiiversion","dataentryid","datacheck"],
    "localstep": ["household"],
    "localthreat": ["household"],
    "marineorganizationmembership": ["household"],
    "nonmarineorganizationmembership": ["household"],
    "mpainterviewyear": [],
    "mpanetwork": [],
    "right": ["kii"],
    "rule": ["fgd"],
    "seascape": [],
    "species": ["fgd"],
    "speciesrule": ["kii"],
    "stakeholder": ["fgd"],
    "users": ["fgd","userextbnd","userintbnd"],
    "zone": ["kii"],
    "monitoringstaff": [],
    "demographic": ["household"],
    "lkpassetobtain": [],
    "lkpassetassistance": [],
    "fgdsurveyversion": [],
    "householdsurveyversion": [],
}

def import_table(datafile, identifier, cleardata, tofile):
    print("importing " + identifier +"...")
    thechoices = get_ingest_project_choices()
    print(identifier)
    themodel = model_choice[identifier]["model"]
    if cleardata:
        themodel.objects.all().delete()
    reader = csv.DictReader(datafile)
    lookuperrors = []
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

    rowcount = 0  # TODO - find better way of getting the row in the csv
    for row in reader:
        rowcount += 1
        for rec in related_records[identifier]:
            if row[rec]:
                try:
                    theval = thechoices["data__"+rec][row[rec]]
                except KeyError:
                    lookuperrors.append([rowcount, row[rec], rec])
                    continue
                row[rec] = theval
            else:
                row[rec] = None

    datafile.seek(0)
    reader = csv.DictReader(datafile)

    if len(lookuperrors):
        print("Import failed")
        display_errors(lookuperrors, tofile, identifier)

    rowcount = 0
    for row in reader:
        rowcount += 1
        row = {key.strip(): value for key, value in row.items()} #some field names have spaces at the end
        for rec in related_records[identifier]:
            if row[rec]:
                row[rec] = thechoices["data__"+rec][row[rec]]

        field_conditions_null = field_conditions(themodel)["nullf"]
        field_conditions_all = field_conditions(themodel)["all"]

        cleaned_row = {k: (v if (v or k not in field_conditions_null) else None) for k, v in row.items()}

        # if field is blank and is not required, remove it from insert array
        for fldtest in field_conditions_null:
            if fldtest in cleaned_row:
                if not cleaned_row[fldtest]:
                    del (cleaned_row[fldtest])

        # if field is blank, is required and has a default, remove it from insert array
        for fldtest in field_conditions_all:
            if not fldtest.null and fldtest.default:
                if fldtest.name in cleaned_row:  # key exists in array
                    if not cleaned_row[fldtest.name]:  # its blank
                        del (cleaned_row[fldtest.name])

        #convert date fields to YYYY-MM-DD if they are in MM-DD-YYYY
        for fldtest in field_conditions_all:
            if fldtest.get_internal_type() == "DateField":
                try:
                    datetime.strptime(cleaned_row[fldtest.name], "%m/%d/%Y")
                    cleaned_row[fldtest.name] = datetime.strptime(cleaned_row[fldtest.name], "%m/%d/%Y").strftime("%Y-%m-%d")
                except:
                    #its not in MM-DD-YYYY
                    pass
        # TODO - how to identify boolean fields and make them python booleans
        for fldtruth in field_conditions_all:
            if fldtruth.name == "dataentrycomplete" or fldtruth.name == "datacheckcomplete":
                cleaned_row[fldtruth.name] = mpatruth[cleaned_row[fldtruth.name]]

        try:
            themodel.objects.create(**cleaned_row)
        except IntegrityError as e:
            print("There was an error in importing row {}. Import failed. See details below.".format(rowcount))
            print(e.args[0])
            sys.exit()
    print("Data imported successfully!")

def get_table_import(table):
    return import_table

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


def field_conditions(themodel):
    nodata_fields = [f.name for f in themodel._meta.local_fields if f.default == NODATA[0] or f.default == str(NODATA[0])]
    null_fields = [f.name for f in themodel._meta.local_fields if f.null]
    blank_fields = [f.name for f in themodel._meta.local_fields if f.blank]
    all_fields = themodel._meta.local_fields

    return {
        "nodataf": nodata_fields,
        "nullf": null_fields,
        "blankf": blank_fields,
        "all": all_fields,
    }


def display_errors(lookuperrors, tofile, identifier):
    if tofile:
        now = datetime.now()
        current_time = now.strftime("%H_%M_%S")
        f = open("importerrors/" + identifier + "_" + current_time + ".txt", "a")
    for error in lookuperrors:
        message = "Record {}: keyerror: cannot find {} {} in the lookup table".format(
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
