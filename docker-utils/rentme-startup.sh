#!/bin/bash

# Makes sure we exit if any command fails.
set -ex

if [ "`id -u`" -eq '0' ]; then
  virtualenv --system-site-packages /venv

  . /venv/bin/activate

  pip install --upgrade pip setuptools wheel

  pip install --upgrade /code

  [[ -x /post-install.sh ]] && /post-install.sh

  su --preserve-environment user -- "$0" "$@"
else
  . /venv/bin/activate

  "$@"
fi
