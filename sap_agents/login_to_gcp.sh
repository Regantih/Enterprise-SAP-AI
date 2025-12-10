#!/bin/bash
./gcloud_sdk/google-cloud-sdk/bin/gcloud auth login --no-launch-browser
echo "✅ Login Complete!"
echo "Now run: ./deploy_to_gcp.sh"
