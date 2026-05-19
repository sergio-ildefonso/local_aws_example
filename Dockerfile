# Use the official Floci compatibility image containing Python and AWS CLI
FROM floci/floci:latest-compat

# (Optional) Pre-create a local S3 bucket or resource upon container ready state
# Floci natively supports LocalStack/Floci initialization hooks
RUN mkdir -p /etc/floci/init/ready.d

# Example init script setup to pre-provision a service
RUN echo '#!/bin/sh' > /etc/floci/init/ready.d/init-aws.sh && \
    echo 'aws s3 mb s3://my-local-bucket' >> /etc/floci/init/ready.d/init-aws.sh && \
    chmod +x /etc/floci/init/ready.d/init-aws.sh

# Expose the unified AWS emulation port
EXPOSE 4566
