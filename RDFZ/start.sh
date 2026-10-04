#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exec node tools/serve_web.mjs
