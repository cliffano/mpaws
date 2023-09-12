#!/bin/sh
set -o nounset

echo "\n\n========================================"
echo "Show warning when MPAWS_PROFILES is not set: mpaws help"
MPAWS_PROFILES= mpaws help

echo "\n\n========================================"
echo "Run command with args: mpaws s3 ls"
MPAWS_PROFILES=profile1,profile2,profile3 mpaws s3 ls
EXIT_CODE=$?
if [ $EXIT_CODE -ne 3 ];
then
  echo "Unexpected exit code: $EXIT_CODE"
  exit $EXIT_CODE
fi
