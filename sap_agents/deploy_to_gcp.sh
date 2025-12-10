#!/bin/bash

# Configuration
PROJECT_ID=$(./gcloud_sdk/google-cloud-sdk/bin/gcloud config get-value project 2>/dev/null)
APP_NAME="antigravity-ai"
REGION="us-central1"
GCLOUD="./gcloud_sdk/google-cloud-sdk/bin/gcloud"

# Check if logged in
if [ -z "$PROJECT_ID" ]; then
    echo "⚠️  Not logged in to Google Cloud."
    echo "Please run: $GCLOUD auth login"
    echo "Then run: $GCLOUD config set project <YOUR_PROJECT_ID>"
    exit 1
fi

echo "🚀 Starting Google Cloud Deployment..."
echo "---------------------------------------"
echo "   Project: $PROJECT_ID"
echo "   App:     $APP_NAME"
echo "   Region:  $REGION"
echo "---------------------------------------"

# 1. Enable Services (First time only)
echo "\n🔧 Step 1: Enabling Cloud Run & Cloud Build APIs..."
$GCLOUD services enable cloudbuild.googleapis.com run.googleapis.com

# 2. Submit Build
echo "\n🏗️  Step 2: Submitting Build to Cloud Build..."
$GCLOUD builds submit --config cloudbuild.yaml .

# 3. Get URL
echo "\n✅ Deployment Complete!"
SERVICE_URL=$($GCLOUD run services describe $APP_NAME --platform managed --region $REGION --format 'value(status.url)')
echo "🌍 Public Demo Link: $SERVICE_URL"
echo "---------------------------------------"
echo "Share this link with your users!"
