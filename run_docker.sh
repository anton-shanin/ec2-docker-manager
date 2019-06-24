#!/usr/bin/env bash
read -p "Enter secret key: " secret_key
read -p "Enter access key: " access_key
docker run -e AWS_ACCESS_KEY="${access_key}" -e AWS_SECRET_KEY="${secret_key}" -dp 6543:6543 ec2_pyramid
