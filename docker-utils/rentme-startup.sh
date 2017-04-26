#!/bin/bash

# Makes sure we exit if any command fails.
set -ex

if [ "`id -u`" -eq '0' ]; then
  rm -f /venv/bin/python /venv/bin/python3
  /usr/local/bin/python3.5 -m virtualenv --python=python3.5 --system-site-packages /venv

  . /venv/bin/activate

  pip install -e /code

  [[ -x /post-install.sh ]] && /post-install.sh

  su --preserve-environment user -- "$0" "$@"
else
  . /venv/bin/activate

  "$@"
fi
