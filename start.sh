#!/bin/bash

# Start Floci AWS emulator in detached mode
echo "Starting Floci AWS emulator..."
docker compose up -d

# Wait for Floci to be ready (optional but recommended)
echo "Waiting for Floci to be ready..."
while ! curl -s http://localhost:4566 > /dev/null; do sleep 1; done
echo "Floci is ready!"

# Initialize and apply Terraform configuration
echo "Initializing Terraform..."
terraform init

echo "Applying Terraform configuration..."
terraform apply --auto-approve

# Setup Python virtual environment and run the DB script
echo "Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Running database management script..."
python db_scripts/manage_db.py

echo "Running S3 management script..."
python s3_scripts/manage_s3.py

echo "Done!"