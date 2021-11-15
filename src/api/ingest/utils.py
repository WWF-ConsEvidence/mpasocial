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
from django.db.models import fields


def import_table(datafile, identifier, cleardata, tofile):
    print("importing " + identifier +"...")
    themodel = apps.get_model("api", identifier)  # identifier comes from command
    related_models = []
    for field in themodel._meta.fields:
        if field.is_relation and field.related_model and field.related_model.__name__ != 'User':  # does not pick up m2m fields
            related_models.append([field.name,field.related_model])
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
            rec = lookup_model[0]
            try:
                lookup_instance = None
                if row[rec]:
                    lookup_instance = lookup_model[1].objects.get(pk=row[rec])
            except lookup_model[1].DoesNotExist:
                lookuperrors.append([rowcount, row[rec], rec])
                continue
            row[rec] = lookup_instance

        # remove fields that are blank
        cleaned_row = {k: v for k, v in row.items() if v}

        #convert date fields to YYYY-MM-DD if they are in MM-DD-YYYY
        for fld_date in themodel._meta.get_fields():
            if fld_date.__class__.__name__ == "DateField":
                try:
                    datetime.strptime(cleaned_row[fld_date.name], "%m/%d/%Y")
                    cleaned_row[fld_date.name] = datetime.strptime(cleaned_row[fld_date.name], "%m/%d/%Y").strftime("%Y-%m-%d")
                except:
                    #its not in MM-DD-YYYY
                    pass
        # TODO - how to identify boolean fields and make them python booleans
        for fld_truth in themodel._meta.get_fields():
            if fld_truth.__class__.__name__ == "BooleanField":
                cleaned_row[fld_truth.name] = mpatruth[cleaned_row[fld_truth.name]]

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
