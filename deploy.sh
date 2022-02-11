#!/bin/sh
PROJECT_ID=$(gcloud config get-value project)
gcloud iam service-accounts create dbadmin --display-name="Cloud Sql Admin"
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable sqladmin.googleapis.com
SSA=dbadmin@$PROJECT_ID.iam.gserviceaccount.com
gcloud iam service-accounts keys create dbadmin.json --iam-account=$SSA
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member serviceAccount:$SSA \
--role=roles/cloudsql.admin
gcloud functions deploy cleanUpDB --runtime python39 --set-env-vars GCP_PROJECT=$PROJECT_ID --trigger-http --allow-unauthenticated

