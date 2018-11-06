# Script to deprovision Synapse External Bucket and related CF Stack
# !! WARNING !! This script will permanently delete the S3 bucket
# Usage:  ./DeleteSynapseExternalBucket.sh $STACK_NAME
#!/usr/bin/env bash
set -e

STACK_NAME=$1
SYNAPSE_BUCKET_NAME=$(aws cloudformation list-exports --query "Exports[?Name=='us-east-1-$STACK_NAME-SynapseExternalBucket'].Value" --output text)
aws s3 rb s3://$SYNAPSE_BUCKET_NAME --force
aws cloudformation delete-stack --stack-name $STACK_NAME
