#!/bin/bash

if [ "${BASH_ARGC}" != 2 ]
then
  echo "usage: commit_tag.sh [comment] [tag]"
  echo ""
  git tag
  exit 0
fi

comment="${BASH_ARGV[1]}"
tag="${BASH_ARGV[0]}"

git add .; git commit -m "${comment}"; git tag "${tag}"; git push -f --tag origin master
