#!/usr/bin/env bash

DOCKER=docker
REPORT_DIR=${1:-~/Downloads/reports}
${DOCKER} run -it --rm -v "${REPORT_DIR}":/data "$(${DOCKER} build -q .)"

open "${REPORT_DIR}/ready"
