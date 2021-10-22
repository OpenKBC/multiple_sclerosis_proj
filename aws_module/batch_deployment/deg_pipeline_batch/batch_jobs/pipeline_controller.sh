#!/bin/bash
#Example: sh pipeline_controller.sh CD4 Sex M F
celltype=$1
condition=$2
cond1=$3
cond2=$4

if [ $AWS_BATCH_JOB_ARRAY_INDEX -eq 0 ];
then
    conda run -n pipeline_controller_base python step1_get_DESeq2_input.py -c $celltype -v $condition -x $cond1 -y $cond2

elif [ $AWS_BATCH_JOB_ARRAY_INDEX -eq 1 ];
then
    conda run -n pipeline_controller_base Rscript step2_DESeq2_calculator.R ${efspoint}${celltype}_output.csv ${efspoint}${celltype}_meta_output.csv ${efspoint}DEG_${celltype}.result

else
    conda run -n pipeline_controller_base python step3_upload_to_s3.py -c $celltype
fi