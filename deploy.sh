#!/bin/sh
PROJECT_ID=$(gcloud config get-value project)
gcloud iam service-accounts create dbadmin --display-name="Cloud Sql Admin"
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable sqladmin.googleapis.com
SSA=dbadmin@$PROJECT_ID.iam.gserviceaccount.com
git clone https://github.com/lcsdovalle/nordcloudghostfunction.git
cd nordcloudghostfunction && gcloud iam service-accounts keys create dbadmin.json --iam-account=$SSA
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member serviceAccount:$SSA \
--role=roles/cloudsql.admin
mv dbadmin.json ./nordcloudghostfunction/ && cd nordcloudghostfunction/
gcloud functions deploy cleanUpDB --runtime python39 --trigger-http --allow-unauthenticated
_URL=$(gcloud functions describe cleanUpDB --format="value(httpsTrigger.url)")
curl -X POST $_URL \
-H 'Content-Type: application/json' \
-d '{"key":"fa47c14adc939ee35190cec22d429263"}' 