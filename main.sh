#!/bin/bash
#$ -S /bin/bash
#$ -N bicodon
#$ -q standard.q
#$ -cwd
#$ -v PATH
#$ -o ./log/bicodon_$JOB_ID_$TASK_ID.out
#$ -e ./log/bicodon_$JOB_ID_$TASK_ID.err
#$ -l mem_free=5G

set -ue

argFilepath=${1}
lineNum=${SGE_TASK_ID:-1}
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
fp_cds=`echo ${line} | cut -d ',' -f1`
fp_bt=`echo ${line} | cut -d ',' -f2`
fp_ii=`echo ${line} | cut -d ',' -f3`

./main.py ${fp_cds} ${fp_bt} ${fp_ii}
