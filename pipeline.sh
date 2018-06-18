#!/bin/bash

set -ue

cmd=main.sh
argCmd=./arg/${cmd%.*}.py
argFilepath=${argCmd%.*}.lst
eval ${argCmd} > ${argFilepath}
numJobs=`grep -c '' ${argFilepath}`
jobid_r=`qsub -terse -t 1-${numJobs} -tc 30 ${cmd} ${argFilepath}`
jobid=`echo ${jobid_r} | cut -d '.' -f1`
echo "submitted ${numJobs} jobs with job_id=${jobid}"
