pip install archerysec-cli

DATE=`date +%Y-%m-%d`

ARCHERY_USER=admin
ARCHERY_PASS=admin

export PROJECT_ID=`archerysec-cli -s ${ARCHERY_HOST} -u ${ARCHERY_USER} -p ${ARCHERY_PASS} --createproject --project_name=DevSecOps --project_disc=PROJECT_DISC --project_start=${DATE}  --project_end=${DATE} --project_owner=test_project | tail -n1 | jq '.project_id' | sed -e 's/^"//' -e 's/"$//'`

export SCAN_ID=`archerysec-cli -s ${ARCHERY_HOST} -u ${ARCHERY_USER} -p ${ARCHERY_PASS} --zapscan --target_url=''${TARGET_URL}'' --project_id=''$PROJECT_ID'' | tail -n1 | jq '.scanid' | sed -e 's/^"//' -e 's/"$//'`

echo "scan id......" $SCAN_ID

python /var/jenkins_home/archery_script.py --scanner=zap_scan --scan_id=$SCAN_ID --username=${ARCHERY_USER} --password=${ARCHERY_PASS} --host=${ARCHERY_HOST} --high=10 --medium=15

export job_status=`python /var/jenkins_home/archery_script.py --scanner=zap_scan --scan_id=$SCAN_ID --username=${ARCHERY_USER} --password=${ARCHERY_PASS} --host=${ARCHERY_HOST} --high=10 --medium=15`

if [ -n "$job_status" ]
then
  #Run your script commands here
   echo "Build Sucess"
else
 echo "BUILD FAILURE: Other build is unsuccessful or status could not be obtained."
 exit 100
fi

