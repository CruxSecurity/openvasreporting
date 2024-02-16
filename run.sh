#!/usr/bin/env bash

for file in /data/*.xml; do
    test ! -r "${file%.xml}.xlsx" &&
        echo "Converting ${file}." &&
        python3 -m openvasreporting -i "${file}" -o "${file%.xml}.xlsx"
done

mkdir -p /data/ready

for file in /data/*; do
    BASENAME=$(basename "${file}")
    cp -fv "${file}" "/data/ready/${BASENAME#*: }"
done
