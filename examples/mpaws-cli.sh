#!/usr/bin/env bash
# set -o errexit
set -o nounset

cd ../
. ./.venv/bin/activate
cd examples/

printf "\n\n========================================\n"
printf "Show help guide:\n"
mpaws --help

printf "\n\n========================================\n"
printf "Show version info: mpaws --version\n"
mpaws --version

printf "\n\n========================================\n"
printf "Run command with args when MPAWS_PROFILES and MPAWS_REGIONS are set:\n"
MPAWS_PROFILES=profile1,profile2,profile3 \
  MPAWS_REGIONS=us-east-1,ap-southeast-2 \
  mpaws ec2 describe-instances

printf "\n\n========================================\n"
printf "Run command with args when MPAWS_PROFILES and MPAWS_REGIONS are set:\n"
MPAWS_PROFILES=profile1,profile2,profile3 \
  MPAWS_REGIONS=us-east-1 \
  mpaws ec2 describe-instances

printf "\n\n========================================\n"
printf "Run command with args when MPAWS_PROFILES and AWS_DEFAULT_REGION are set:\n"
MPAWS_PROFILES=profile1,profile2,profile3 \
  AWS_DEFAULT_REGION=us-east-1 \
  mpaws ec2 describe-instances

printf "\n\n========================================\n"
printf "Run command with args when MPAWS_PROFILES and AWS_REGION are set:\n"
MPAWS_PROFILES=profile1,profile2,profile3 \
  AWS_REGION=us-east-1 \
  mpaws ec2 describe-instances

printf "\n\n========================================\n"
printf "Run command with custom shell command:\n"
MPAWS_PROFILES=profile1,profile2,profile3 \
  AWS_REGION=us-east-1 \
  mpaws _ echo \$\{AWS_REGION\}
