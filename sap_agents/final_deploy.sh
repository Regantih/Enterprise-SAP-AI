#!/bin/bash

# Hardcoded Configuration
PROJECT_ID="valid-heuristic-477801-h3"
GCLOUD="./gcloud_sdk/google-cloud-sdk/bin/gcloud"

echo "🚀 Starting Auto-Deployment..."
echo "-----------------------------"

# 1. Check Login
ACCOUNT=$($GCLOUD auth list --filter=status:ACTIVE --format="value(account)")
if [ -z "$ACCOUNT" ]; then
    echo "⚠️  You are not logged in."
    echo "👉 INSTRUCTIONS:"
    echo "1. Copy the link below and open it in your browser."
    echo "2. Log in with your Google Account."
    echo "3. When you see a 'This site can't be reached' (localhost) error:"
    echo "   ➡️ COPY THE ENTIRE URL from your browser's address bar."
    echo "   ➡️ PASTE that URL here."
    $GCLOUD auth login --no-browser
fi

# 2. Set Project
echo "\n⚙️  Setting Project to: $PROJECT_ID"
$GCLOUD config set project $PROJECT_ID

# 3. Enable APIs
echo "\n🔧 Enabling Cloud Services..."
$GCLOUD services enable cloudbuild.googleapis.com run.googleapis.com

# 4. Deploy
echo "\n🏗️  Building and Deploying..."
$GCLOUD builds submit --config cloudbuild.yaml .

# 5. Get URL
SERVICE_URL=$($GCLOUD run services describe antigravity-ai --platform managed --region us-central1 --format 'value(status.url)')

echo "\n✅ SUCCESS!"
echo "---------------------------------------"
echo "🌍 YOUR DEMO LINK: $SERVICE_URL"
echo "---------------------------------------"
