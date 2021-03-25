#!/bin/bash

set -evx

site=$1
shift 1

logs=$site/logs
done=$logs/done
log=$logs/parallel.$(date --iso-8601=seconds)

yard_files=$(ls --almost-all /farm/yard/*.tmp | wc --lines)

if [[ "${yard_files}" != "0" ]]; then
    echo /farm/yard is not empty
    exit 1
fi

mkdir -p $logs

parallel --eta --jobs 3 --delay $((3 * 60 * 60)) --max-replace-args 1 bash single "${site}" "{0}" ::: "$@" &>> "${log}"
mkdir -p $done
mv "${log}" ${done}"
