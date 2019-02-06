#!/bin/bash

set -ue

cmd=freqs.sh
arg=./arg/${cmd%.*}.lst
num=`grep -c '' ${arg}`
jobid_r=`qsub -terse -t 1-${num} -tc 30 ${cmd} ${arg}`
jobid=`echo ${jobid_r} | cut -d '.' -f1`
echo "submitted ${num} jobs with job_id=${jobid}"

