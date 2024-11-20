#!/usr/bin/env bash
docker run -it --rm -v "${1:-~/Downloads/reports}":/data "$(docker build -q .)"

open "${1-~/Downloads/reports/ready}"
