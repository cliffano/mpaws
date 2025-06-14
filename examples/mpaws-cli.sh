#!/usr/bin/env bash
set -o errexit
set -o nounset

printf "\n\n========================================\n"
printf "Show version info: mpaws --version\n"
mpaws --version

printf "\n\n========================================\n"
printf "Run command with args when MPAWS_PROFILES and MPAWS_REGIONS are set: mpaws s3 ls\n"
MPAWS_PROFILES=profile1,profile2,profile3 \
  MPAWS_REGIONS=us-east-1,ap-southeast-2 \
  mpaws ec2 describe-instances

printf "\n\n========================================\n"
printf "Run command with args when MPAWS_PROFILES and MPAWS_REGIONS are set: mpaws s3 ls\n"
MPAWS_PROFILES=profile1,profile2,profile3 \
  MPAWS_REGIONS=us-east-1 \
  mpaws ec2 describe-instances

printf "\n\n========================================\n"
printf "Run command with args when MPAWS_PROFILES and AWS_DEFAULT_REGION are set: mpaws s3 ls\n"
MPAWS_PROFILES=profile1,profile2,profile3 \
  AWS_DEFAULT_REGION=us-east-1 \
  mpaws ec2 describe-instances

printf "\n\n========================================\n"
printf "Run command with args when MPAWS_PROFILES and AWS_REGION are set: mpaws s3 ls\n"
MPAWS_PROFILES=profile1,profile2,profile3 \
  AWS_REGION=us-east-1 \
  mpaws ec2 describe-instances
