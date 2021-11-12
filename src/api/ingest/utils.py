import csv
import json
from django.db import connection, transaction, IntegrityError
import datetime
from django.apps import apps
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime
import sys
from api.models.base import *
from api.models.household import *
from api.models.fgd import *
from api.models.kii import *


def import_table(datafile, identifier, cleardata, tofile):
    print("importing " + identifier +"...")
    themodel = apps.get_model("api", identifier)  # identifier comes from command
    related_models = []
    for field in MPA._meta.fields:
        if field.is_relation and field.related_model:  # does not pick up m2m fields
            related_models.append(field.related_model)

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

    rowcount = 0
    for row in reader:
        rowcount += 1
        row = {key.strip(): value for key, value in row.items()}  # some field names have spaces at the end
        for lookup_model in related_models:
            rec = lookup_model.__name__
            try:
                lookup_instance = lookup_model.objects.get(pk=row[rec])
            except lookup_model.DoesNotExist:
                lookuperrors.append([rowcount, row[rec], rec])
                continue
            row[rec] = lookup_instance

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

    if len(lookuperrors):
        print("Import failed")
        display_errors(lookuperrors, tofile, identifier)
    else:
        print("Data imported successfully!")

def get_table_import(table):
    return import_table

def reset_pk(seq, start, identifier):
    themodel = apps.get_model("api", identifier)
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
