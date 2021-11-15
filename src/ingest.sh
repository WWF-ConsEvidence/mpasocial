#! /bin/bash
set -u
echo "Starting ingestion"


echo "Clearing tables"
python manage.py clear_models

for table in "mpa" "settlement" "kii" "lkpassetobtain" "lkpassetassistance" "householdsurveyversion"  "birth" "death" "demographic" "fgdsurveyversion" "fgd" "globalstep" "globalthreat" "habitat" "kiisurveyversion" "lkpfishtechcategory" "lkpfishtechnique" "lkpfreqfishtime"  "lkplivelihood" "household" "habitatrule"
do
  python manage.py import_data importdata/$table.csv --table $table --clear-existing
done