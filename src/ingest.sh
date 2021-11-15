#! /bin/bash
set -u
echo "Starting ingestion"


echo "Clearing tables"
python manage.py clear_models

for table in "mpa" "kii" "settlement" "lkpassetobtain" "lkpassetassistance"  "householdsurveyversion" "household" "birth" "death" "demographic" "fgdsurveyversion" "fgd"  "globalstep" "globalthreat" "habitat" "kiisurveyversion" "lkpfishcategory" "lkpfishtechnique" #"habitatrule"
do
  python manage.py import_data importdata/$table.csv --table $table --clear-existing
done