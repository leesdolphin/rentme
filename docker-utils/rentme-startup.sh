#!/bin/bash

# Makes sure we exit if any command fails.
set -ex

pip install --upgrade /code

[[ -x /post-install.sh ]] && /post-install.sh

$@
