#!/bin/bash

# Makes sure we exit if any command fails.
set -ex

if [ "`id -u`" -eq '0' ]; then
  /venv/bin/pip3 install -e /code

  echo "$@"

  if [[ "x$1" == "x--root" ]]; then
    shift
    "$@"
    exit $?
  else
    su user -- "$0" "$@"
  fi
else
  . /venv/bin/activate;

  "$@"
fi
