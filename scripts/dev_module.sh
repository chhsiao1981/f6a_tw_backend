#!/bin/bash


if [ "${BASH_ARGC}" != "1" ]
then
  echo "usage: scripts/dev_module.sh [module (a.b.c)]"
  exit 0
fi

module=${BASH_ARGV[0]}

echo "[INFO] to create module: ${module}"
pcreate -s module . ${module}

parent_pkg=""
# split module
arr=$(echo ${module}|tr "." "\n")

# setup 
for each_pkg in ${arr[@]}
do
  echo "each_pkg: ${each_pkg}"
  if [ "${parent_pkg}" != "" ]
  then
    echo "[INFO] to create pkg: ${parent_pkg}"
    pcreate -s pkg . ${parent_pkg}
    parent_pkg="${parent_pkg}."
  fi
  parent_pkg="${parent_pkg}${each_pkg}"
done
