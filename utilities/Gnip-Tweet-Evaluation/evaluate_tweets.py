#!/usr/bin/env python

import argparse
try:
    import ujson as json 
except ImportError:
    import json
import sys
import datetime

from gnip_tweet_evaluation import analysis,output

##
## analysis functions
##

def run_analysis(input_generator, conversation_results, audience_results): 
    """ iterate over Tweets and analyze"""
    user_ids = set()
    for line in input_generator: 
        try:
            tweet = json.loads(line)  
        except ValueError:
            continue
        
        # account for compliance and other non-standard tweet payloads
        if "actor" not in tweet:
            continue
        if conversation_results is not None:
            analysis.analyze_tweet(tweet,conversation_results)
        if audience_results is not None:
            user_id = int(tweet["actor"]["id"].split(":")[2])
            if user_id not in user_ids:
                analysis.analyze_bio(tweet,audience_results)
                user_ids.add( user_id ) 
        
    if audience_results is not None:
        analysis.analyze_user_ids(user_ids,audience_results)
    
    return user_ids

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--identifier",dest="unique_identifier", default=None,
            help="a unique name to identify the conversation/audience")
    parser.add_argument("-c","--do-conversation-analysis",dest="do_conversation_analysis",action="store_true",default=False,
            help="do conversation analysis on Tweets")
    parser.add_argument("-a","--do-audience-analysis",dest="do_audience_analysis",action="store_true",default=False,
            help="do audience analysis on users") 
    parser.add_argument("-i","--input-file-name",dest="input_file_name",default=None,
            help="file containing tweets, tweet IDs, or user IDs; take input from stdin if not present")
    args = parser.parse_args()

    # get the time right now, to use in output naming
    time_string = datetime.datetime.now().isoformat().split(".")[0].translate(None,":")

    # creat dictionaries for results requested
    # entries in these dictionaries map measurement names to data collections
    # start by creating a unique ID from the audience/conversation identifier and the current time
    if args.do_audience_analysis:
        audience_results = {"unique_id": args.unique_identifier + "_" + time_string} 
    else:
        audience_results = None
    if args.do_conversation_analysis:
        conversation_results = {"unique_id": args.unique_identifier + "_" + time_string} 
    else:
        conversation_results = None

    # manage input source
    if args.input_file_name is not None:
        input_generator = open(args.input_file_name)
    else:
        input_generator = sys.stdin

    # run analysis
    run_analysis(input_generator,conversation_results,audience_results)

    # format and dump results
    if args.do_conversation_analysis:
        analysis.summarize_tweets(conversation_results)
        output.dump_conversation(conversation_results)
    if args.do_audience_analysis:
        analysis.summarize_audience(audience_results)
        output.dump_audience(audience_results)
