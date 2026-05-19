# Local AWS Emulation with Floci

This project sets up a local AWS emulation environment using Floci, a fast, Quarkus-native emulator that acts as an alternative to LocalStack.

## Files Overview

- **`docker-compose.yaml`**: Defines the `floci` service directly using the `floci/floci:latest-compat` image. It configures environment variables, exposes port `4566` for standard API access and `7001` for the RDS engine, and mounts the Docker socket.
- **`start.sh`**: A convenience script that spins up the Docker container, waits for Floci to be ready, applies the Terraform configuration, sets up the Python virtual environment, installs dependencies, and runs the initial database and S3 population scripts.
- **`db_scripts/manage_db.py`**: A Python script that connects to the local PostgreSQL database, creates the `countries` table, and seeds it with initial data.
- **`s3_scripts/manage_s3.py`**: A Python script that connects to the local S3 endpoint to upload a file, copy it to a different bucket, and list its contents.
- **`requirements.txt`**: Contains Python dependencies (such as `awscli-local` and `psycopg2-binary`) required to interact with the local AWS emulator and database.
- **`main.tf`**: Contains the Terraform configuration to provision infrastructure on the local AWS emulator (3 S3 buckets, an RDS PostgreSQL database, and 2 Lambda functions).


## Prerequisites

- Docker and Docker Compose.
- [Terraform](https://developer.hashicorp.com/terraform/downloads) installed to provision resources locally.
- Python 3.x and `venv` to install the dependencies locally.

## Local Setup

To interact with the local emulator easily, install the required Python tools (like `awslocal`) in a virtual environment:

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. **Start the environment and provision resources:**
   The easiest way to get started is to use the provided setup script. It will start the Docker container in detached mode, run Terraform to provision the initial infrastructure (S3, Lambda, RDS), setup a Python virtual environment to install dependencies, and finally run `manage_db.py` and `manage_s3.py` to seed the database and populate S3 buckets:
   ```bash
   ./start.sh
   ```

2. **Verify it's running:**
   Check the logs to ensure the emulator started successfully:
   ```bash
   docker-compose logs -f
   ```

3. **Interact with local AWS services:**
   Use the AWS CLI or `awslocal` to manage resources. For example, to list the newly created S3 buckets:
   ```bash
   awslocal s3 ls
   ```

## Configuration Details

Key environment variables configured in `docker-compose.yaml`:
- `FLOCI_STORAGE_MODE=persistent`: Keeps state across container restarts.
- Dummy standard AWS credentials (`AWS_DEFAULT_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) are set up for smooth local SDK initialization.

