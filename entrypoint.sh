#!/usr/bin/env bash

mkdir ~/.aws
echo [default]$'\n'aws_secret_access_key="$AWS_SECRET_KEY"$'\n'aws_access_key_id="$AWS_ACCESS_KEY" > ~/.aws/credentials
echo [default]$'\n'region=us-west-2 > ~/.aws/config
pserve production.ini