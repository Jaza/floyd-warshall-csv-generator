#!/bin/bash
set -e

if [[ ! -x "$(command -v curl)" ]]; then
  apt-get update && apt-get install -y curl
fi

set +e
