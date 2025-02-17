#!/bin/sh

function die { echo $1: status $2 ; exit $2; }

if [ "${SCRAM_TEST_NAME}" != "" ] ; then
  mkdir ${SCRAM_TEST_NAME}
  cd ${SCRAM_TEST_NAME}
fi
if test -f "SiStripConditionsDBFile.db"; then
    echo "cleaning the local test area"
    rm -fr SiStripConditionsDBFile.db  # builders test
    rm -fr modifiedSiStrip*.db         # miscalibrator tests
    rm -fr gainManipulations.db        # rescaler tool
fi
pwd
echo " testing CondTools/SiStrip"

# do the builders first (need the input db file)
for entry in "${LOCAL_TEST_DIR}/"SiStrip*Builder_cfg.py
do
  echo "===== Test \"cmsRun $entry \" ===="
  (cmsRun $entry) || die "Failure using cmsRun $entry" $?
done

echo -e " Done with the writers \n\n"

## do the readers
for entry in "${LOCAL_TEST_DIR}/"SiStrip*Reader_cfg.py
do
  echo "===== Test \"cmsRun $entry \" ===="
  (cmsRun $entry) || die "Failure using cmsRun $entry" $?
done

echo -e " Done with the readers \n\n"

sleep 5

## do the builders from file
for entry in "${LOCAL_TEST_DIR}/"SiStrip*FromASCIIFile_cfg.py
do
  echo "===== Test \"cmsRun $entry \" ===="
  (cmsRun $entry) || die "Failure using cmsRun $entry" $?
done

echo -e " Done with the builders from file \n\n"

## do the miscalibrators
for entry in "${LOCAL_TEST_DIR}/"SiStrip*Miscalibrator_cfg.py
do
  echo "===== Test \"cmsRun $entry \" ===="
  (cmsRun $entry) || die "Failure using cmsRun $entry" $?
done

echo -e " Done with the miscalibrators \n\n"

## do the scaler

# copy all the necessary conditions in order to run the miscalibration tool
G1TAG=SiStripApvGain_GR10_v1_hlt
G2TAG=SiStripApvGain_FromParticles_GR10_v1_express
OLDG1since=325642
NEWG1since=343828
OLDG2since=336067

echo -e "\n\n Copying IOVs $OLDG1since and $NEWG1since from $G1TAG and IOV $OLDG2since from $G2TAG"

conddb --yes --db pro copy ${G1TAG} G1_old --from ${OLDG1since} --to $((++OLDG1since)) --destdb gainManipulations.db
conddb --yes --db pro copy ${G1TAG} G1_new --from ${NEWG1since} --to $((++NEWG1since)) --destdb gainManipulations.db
conddb --yes --db pro copy ${G2TAG} G2_old --from ${OLDG2since} --to $((++OLDG2since)) --destdb gainManipulations.db

sqlite3 gainManipulations.db "update IOV SET SINCE=1 where SINCE=$((--OLDG1since))" # sets the IOV since to 1
sqlite3 gainManipulations.db "update IOV SET SINCE=1 where SINCE=$((--NEWG1since))" # sets the IOV since to 1
sqlite3 gainManipulations.db "update IOV SET SINCE=1 where SINCE=$((--OLDG2since))" # sets the IOV since to 1

echo -e "\n\n Checking the content of the local conditions file \n\n"
sqlite3 gainManipulations.db "select * from IOV"

(cmsRun ${LOCAL_TEST_DIR}/SiStripApvGainRescaler_cfg.py additionalConds=sqlite_file:${PWD}/gainManipulations.db) || die "Failure using cmsRun SiStripApvGainRescaler_cfg.py)" $?
echo -e " Done with the gain rescaler \n\n"
