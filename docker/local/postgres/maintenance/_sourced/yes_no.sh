#!/bin/bash


yes_no() {
  declare desc="Prompt for confirmation. \$\"\{1\}\": confirm message"

  local arg1="${1}"
  local response=read -r -p "${arg1} (y/[n])? " response

  if [[ "${response}" =~ ^[Yy]$ ]]
  then
    exit 0
  else
    exit 1
  fi
}