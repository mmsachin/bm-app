Connect to Cloud Shell

In your Cloud Shell, make sure you're in the correct directory and have the updated files:
cd ~/bm-app

Udpate the new code in app.py
nano app.py

[replace the old code with new code]
Save and exit ( CTRL + X, y and Enter)

# Build the container
gcloud builds submit --tag gcr.io/alert-synapse-450214-e2/budget-app

# Deploy to Cloud Run
gcloud run deploy budget-app \
  --image gcr.io/alert-synapse-450214-e2/budget-app \
  --platform managed \
  --region us-west1 \
  --allow-unauthenticated
