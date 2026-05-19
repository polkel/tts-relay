#!/usr/bin/env bash

set -Eeuo pipefail

echo "Starting tts-relay deploy..."

ROOT_DIR="$(cd "$(dirname ${BASH_SOURCE[0]})" && cd .. && pwd)"

bash "$ROOT_DIR/deploy/packages.sh"