#!/usr/bin/env bash
# utility to download historical data set from S3
waitForNProcs()
{
  #  procName set prior to calling e.g. procName=$xmlparser
  nprocs=$(pgrep -f $procName | wc -l)
  while [ $nprocs -gt $MAXPROCS ]; do
	sleep $SLEEPTIME
  	nprocs=$(pgrep -f $procName | wc -l)
  done
}
# Configure
SLEEPTIME=15   # seconds
MAXPROCS=8     # cores?
procName=curl
# to run different directory, update these
# Auto updated: 2016-05-27 11:42:04.901187
# AUTOPATH=.
AUTOPATH=/Users/scompston/final_unilever/TAP-Workshop/utilities/Gnip-Python-Historical-Utilities/src
#
export PYTHONPATH=${PYTHONPATH}:$AUTOPATH
mangler="$AUTOPATH/name_mangle.py"

if [ ! -e ./data ]; then
  mkdir ./data
fi

echo "Starting download at $(date)"
echo "Generating file location for $(wc -l ./data_files.txt) files:"

# get final file names
cat ./data_files.txt | $mangler > data_files_tmp.txt

# copy files
echo "Copying $(wc -l ./data_files.txt) files:"
while read fn_tuple; do
    # comment-out waitForNProcs if your files are small
    waitForNProcs
    $procName `echo $fn_tuple | awk '{print $1}'` --create-dirs -o ./data/`echo $fn_tuple | awk '{print $2}'` &
    echo "  copying file $fn to $filen..."
done < ./data_files_tmp.txt
rm -f data_files_tmp.txt

echo "Download completed at $(date)"
