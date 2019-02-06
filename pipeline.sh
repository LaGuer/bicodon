#!/bin/bash

set -ue

#cmd=wget.sh
cmd=freqs.sh

arg_cmd=./arg/${cmd%.*}.py
arg_fp=./arg/${cmd%.*}.lst
eval ${arg_cmd} ${arg_fp}
num=`grep -c '' ${arg_fp}`
jobid_r=`qsub -terse -t 1-${num} -tc 30 ${cmd} ${arg_fp}`
jobid=`echo ${jobid_r} | cut -d '.' -f1`
echo "submitted ${num} jobs with job_id=${jobid}"

