#!/bin/sh
set -o nounset

echo "\n\n========================================"
echo "Show warning when MPAWS_PROFILES is not set: mpaws help"
MPAWS_PROFILES= \
  mpaws help

echo "\n\n========================================"
echo "Show warning when MPAWS_PROFILES, MPAWS_REGIONS, AWS_DEFAULT_REGION, and AWS_REGION are not set: mpaws help"
MPAWS_PROFILES= \
  MPAWS_REGIONS= \
  AWS_DEFAULT_REGION= \
  AWS_REGION= \
  mpaws help

echo "\n\n========================================"
echo "Show warning when MPAWS_PROFILES is set but MPAWS_REGIONS, AWS_DEFAULT_REGION, and AWS_REGION are not set: mpaws help"
MPAWS_PROFILES=profile1,profile2 \
  MPAWS_REGIONS= \
  AWS_DEFAULT_REGION= \
  AWS_REGION= \
  mpaws help

echo "\n\n========================================"
echo "Show warning when MPAWS_PROFILES is not set but MPAWS_REGIONS is set: mpaws help"
MPAWS_PROFILES= \
  MPAWS_REGIONS=us-east-1,ap-southeast-2 \
  mpaws help

echo "\n\n========================================"
echo "Show warning when MPAWS_PROFILES and MPAWS_REGIONS are not set but AWS_DEFAULT_REGION is set: mpaws help"
MPAWS_PROFILES= \
  MPAWS_REGIONS= \
  AWS_DEFAULT_REGION=us-east-1 \
  mpaws help

echo "\n\n========================================"
echo "Show warning when MPAWS_PROFILES and MPAWS_REGIONS are not set but AWS_REGION is set: mpaws help"
MPAWS_PROFILES= \
  MPAWS_REGIONS= \
  AWS_REGION=us-east-1 \
  mpaws help
