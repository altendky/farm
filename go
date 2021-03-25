#!/bin/bash

set -evx

site=$1
shift 1

logs=$site/logs
done=$logs/done
log=$logs/parallel.$(date --iso-8601=seconds)

scratch_files=$(ls --almost-all /scratch | wc --lines)

if [[ "${scratch_files}" != "0" ]]; then
    echo /scratch is not empty
    exit 1
fi

mkdir -p $logs

parallel --eta --jobs 3 --delay $((3 * 60 * 60)) --max-replace-args 1 bash single "${site}" "{0}" ::: "$@" &>> "${log}"
mkdir -p $done
mv "${log}" ${done}"
