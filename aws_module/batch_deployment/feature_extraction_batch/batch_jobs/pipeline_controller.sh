#!/bin/bash
#Example: sh pipeline_controller.sh

if [ $AWS_BATCH_JOB_ARRAY_INDEX -eq 0 ];
then
    conda run -n pipeline_controller_base python step0_downloadFile.py

elif [ $AWS_BATCH_JOB_ARRAY_INDEX -eq 1 ];
then
    conda run -n pipeline_controller_base python step1_cleanup_normalized_matrix.py --vst

elif [ $AWS_BATCH_JOB_ARRAY_INDEX -eq 2 ];
then
    conda run -n pipeline_controller_base python step2_IDconverter.R 

elif [ $AWS_BATCH_JOB_ARRAY_INDEX -eq 3 ];
then
    conda run -n pipeline_controller_base python step3_get_all_activation_scores.py

elif [ $AWS_BATCH_JOB_ARRAY_INDEX -eq 4 ];
then
    conda run -n pipeline_controller_base python step4_actscoreDiff.py --type RR,CIS

elif [ $AWS_BATCH_JOB_ARRAY_INDEX -eq 5 ];
then
    conda run -n pipeline_controller_base python step5_actscoreRFECV.py --type RR,CIS --rthresh 10

elif [ $AWS_BATCH_JOB_ARRAY_INDEX -eq 6 ];
then
    conda run -n pipeline_controller_base python step6_geneDiff.py --type RR,CIS

elif [ $AWS_BATCH_JOB_ARRAY_INDEX -eq 7 ];
then
    conda run -n pipeline_controller_base python step7_geneRFECV.py --type RR,CIS --rthresh 5

else
    conda run -n pipeline_controller_base python step8_upload_to_s3.py
fi