#!/bin/bash
#$ -S /bin/bash
#$ -N freqs
#$ -q standard.q
#$ -cwd
#$ -v PATH
#$ -o ./log/freqs_$JOB_ID_$TASK_ID.out
#$ -e ./log/freqs_$JOB_ID_$TASK_ID.err

argFilepath=${1}
lineNum=${SGE_TASK_ID:-1}
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
cds_fp=`echo ${line} | cut -d ',' -f1`
freqs_fp=`echo ${line} | cut -d ',' -f2`

./freqs.py ${cds_fp} ${freqs_fp}
