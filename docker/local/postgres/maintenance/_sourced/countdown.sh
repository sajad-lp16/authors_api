#!/bin/bash

countdown() {
  declare desc="A Simple Countdown."

  local seconds="${1}"
  local d=$(($(date +%s) + "${seconds}"))

  while [ "$d" -gt `date +%s` ]; do
    echo -ne "$(date -u --date @$(($d - `date +%s`)) +%H:%M:%S)\r";
    sleep 0.1
  done
}