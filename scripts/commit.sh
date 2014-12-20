#!/bin/bash

if [ "${BASH_ARGC}" != 2 ]
then
  echo "usage: commit.sh [comment] [branch]"
  exit 0
fi

comment="${BASH_ARGV[1]}"
branch="${BASH_ARGV[0]}"

git add .; git commit -m "${comment}"; git push origin "${branch}"
