#!/bin/bash
GCLOUD="./gcloud_sdk/google-cloud-sdk/bin/gcloud"

echo "🚀 Google Cloud Setup Wizard"
echo "----------------------------"

# 1. Login
echo "\n🔑 Step 1: Authentication"
echo "You will see a link below. Copy it to your browser, login, and copy the verification code."
echo "Then paste the code back here."
$GCLOUD auth login --no-browser

# 2. List Projects
echo "\n📋 Step 2: Select Project"
echo "Fetching your projects..."
$GCLOUD projects list

echo "\n👉 Enter your PROJECT_ID from the list above:"
read PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    echo "❌ No Project ID entered. Exiting."
    exit 1
fi

# 3. Set Project
$GCLOUD config set project $PROJECT_ID

echo "\n✅ Setup Complete!"
echo "Project set to: $PROJECT_ID"
echo "Now run: ./deploy_to_gcp.sh"
