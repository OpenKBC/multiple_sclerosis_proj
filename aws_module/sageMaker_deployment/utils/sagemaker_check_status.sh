InstanceID=$1
objStatus=dummy

while [ "$objStatus" != "InService" ];do # EC2 running checking
    sleep 1
    objStatus=$(aws sagemaker describe-notebook-instance --notebook-instance-name $InstanceID | jq --jsonargs '.NotebookInstanceStatus')
    objStatus="${objStatus%\"}" # Remove double quotes from string
    objStatus="${objStatus#\"}" # Remove double quotes from string
    echo "Notebook Instance status : $objStatus .."
done