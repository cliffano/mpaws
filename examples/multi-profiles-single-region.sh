#!/bin/sh
set -o nounset

echo "\n\n========================================"
echo "Run command with args when MPAWS_PROFILES and MPAWS_REGIONS are set: mpaws s3 ls"
MPAWS_PROFILES=profile1,profile2,profile3 \
  MPAWS_REGIONS=us-east-1 \
  mpaws ec2 describe-instances

echo "\n\n========================================"
echo "Run command with args when MPAWS_PROFILES and AWS_DEFAULT_REGION are set: mpaws s3 ls"
MPAWS_PROFILES=profile1,profile2,profile3 \
  AWS_DEFAULT_REGION=us-east-1 \
  mpaws ec2 describe-instances

echo "\n\n========================================"
echo "Run command with args when MPAWS_PROFILES and AWS_REGION are set: mpaws s3 ls"
MPAWS_PROFILES=profile1,profile2,profile3 \
  AWS_REGION=us-east-1 \
  mpaws ec2 describe-instances
