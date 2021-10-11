#!/bin/bash

# Warning: This script must be run from project root

APP="mpasocial"
BUCKET="mpasocial-app-versions"
# Defaults that can be overridden with args
PROFILE="mpasocial" # must be defined in ~/.aws/config
ENV="dev"

while getopts ":e:p:" opt; do
  case "${opt}" in
  e)
    ENV=${OPTARG}
    ;;
  p)
    PROFILE=${OPTARG}
    ;;
  \?)
    echo "Invalid option: -$OPTARG" >&2
    ;;
  esac
done
shift "$((OPTIND - 1))"

echo "${PROFILE}"
echo "${ENV}"

echo "Creating archive..."
# Make sure to commit local changes first; this will create zip of latest commit, respecting .gitignore
git archive -o ${APP}.zip HEAD
# remove `docker-compose` so that EB deploys only using Dockerfile
zip -d ${APP}.zip "docker-compose.yml"

STAMP=$(date +%Y%m%d%H%M%S)
COMMIT=$(git rev-parse --verify HEAD)

echo "Uploading..."
aws s3 cp ${APP}.zip s3://${BUCKET}/${APP}-${ENV}-${COMMIT}-${STAMP}.zip --profile=${PROFILE}

echo "Updating Elastic Beanstalk..."
aws elasticbeanstalk create-application-version --profile=${PROFILE} --application-name "${APP}" \
  --version-label "${APP}-${ENV}-${COMMIT}-${STAMP}.zip" \
  --source-bundle S3Bucket="${BUCKET}",S3Key="${APP}-${ENV}-${COMMIT}-${STAMP}.zip"

aws elasticbeanstalk update-environment --profile=${PROFILE} --environment-name "${APP}-${ENV}" \
  --version-label "${APP}-${ENV}-${COMMIT}-${STAMP}.zip"

echo "Cleaning up"
rm ${APP}.zip
cd ../
