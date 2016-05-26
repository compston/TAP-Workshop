#!/bin/bash

#
# a script for running over data stored in a particular location,
# enriching, and analyzing the tweets.
#

base_path=data/

# use this to label all output files from a particular project or
# working directory, especially if the output are in a shared space.
output_uid=xxyyzz
input_uid=aabbcc

# loop over these values
day_list=`seq -f%02g 1 31`
month_list="12"
year_list="2015"

MAXPROCS=8
SLEEPTIME=2
procName="enricher"

waitForNProcs()
{
  # procName set prior to calling e.g. procName=$xmlparser
  # set MAXPROCS to the number of procs... (ge because pgrep  has 1 extra line)
  nprocs=$(pgrep -f $procName -U ${UID} | wc -l)
  while [ $nprocs -ge $MAXPROCS ]; do
    sleep $SLEEPTIME
    nprocs=$(pgrep -f $procName -U ${UID} | wc -l)
  done
}

for year in $year_list; do
    for month in $month_list; do
        for day in $day_list; do
#            mkdir -p data/${year}/${month}/${day}
            
            # Set up your processing here:
            # You might just run the enricher,
            # or just run the aggregator on enriched data.
            # Below is the full processing pipeline for daily data
            
            zcat /mnt/Compston/20150101-20160101_pm1pv2v8ck_2015_12_${day}*activities.json.gz | nice ./enricher.py > /mnt/Compston/enriched_tweets/2015_12_${day}_enriched.json
	    sleep 1

            #input_file=data/tweets_${input_uid}.json.gz
            #if [[ "$input_file" != "" ]]; then
            #    output_file=data/data_${output_uid}.pkl
            #    zcat $input_file | nice ./enricher.py | ./aggregator.py > $output_file &
            #    sleep 1 # sometimes helpful to slow down the initial spinup of processes
            #fi
            waitForNProcs
        done
    done
done 
wait
