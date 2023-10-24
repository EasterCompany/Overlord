#!/bin/sh
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
  echo "0"
elif [ $LOCAL = $BASE ]; then
  echo "1"
elif [ $REMOTE = $BASE ]; then
  echo "2"
else
  echo "3"
fi

