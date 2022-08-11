#!/bin/bash
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
  echo "1"
elif [ $LOCAL = $BASE ]; then
  echo "                              Need to Pull"
elif [ $REMOTE = $BASE ]; then
  echo "                              Need to Push"
else
  echo "                          Diverged from Branch"
fi
