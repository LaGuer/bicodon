#!/bin/bash
#$ -S /bin/bash
#$ -N wget
#$ -q standard.q
#$ -cwd
#$ -v PATH
#$ -o ./log/wget_$JOB_ID_$TASK_ID.out
#$ -e ./log/wget_$JOB_ID_$TASK_ID.err

argFilepath=${1}
lineNum=${SGE_TASK_ID:-1}
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
ftp=`echo ${line} | cut -d ',' -f1`
out=`echo ${line} | cut -d ',' -f2`

wget --timeout 120 --no-verbose -O - ${ftp} | gunzip -c > ${out}
