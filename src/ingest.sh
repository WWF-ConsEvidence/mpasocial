#! /bin/bash
set -u
echo "Starting ingestion"


echo "Clearing tables"
python manage.py clear_models

for table in \
  "monitoringstaff" \
  "mpanetwork" \
  "seascape" \
  "mpa" \
  "mpainterviewyear" \
  "settlement" \
  "fgdsurveyversion" \
  "fgd" \
  "kii" \
  "lkpassetobtain" \
  "lkpassetassistance" \
  "householdsurveyversion"  \
  "birth" \
  "death" \
  "demographic" \
  "globalstep" \
  "globalthreat" \
  "habitat" \
  "kiisurveyversion" \
  "lkpfishtechcategory" \
  "lkpfishtechnique" \
  "lkpfreqfishtime"  \
  "lkplivelihood" \
  "lkpnonetoallscale" \
  "localstep" \
  "localthreat" \
  "marineorganizationmembership" \
  "nonmarineorganizationmembership" \
  "household" \
  "habitatrule" \
  "right" \
  "rule" \
  "species" \
  "speciesrule" \
  "stakeholder" \

do
  python manage.py import_data importdata/$table.csv --table $table --clear-existing
done