#!/usr/bin/env python

import importlib
import sys
import argparse
import logging
import ConfigParser
from math import log10, floor

import models
import time_bucket

def analyze(generator, model, rule_name = None, return_queue = None, logr = None): 
    """
    This function loops over the items generated by the generator from the first argument.
    The expected format for each item is: [TimeBucket] [count]
    Each count is used to update the model, and the model result is added to the return list.
    """
    plotable_data = [] 
    for line in generator:
        time_bucket = line[0]
        count = line[1]
        
        model.update(count=count, time_bucket=time_bucket)
        result = float(model.get_result())
        
        if count > 0:
            trimmed_count = round(count, -int(floor(log10(count)))+3) 
        else:
            trimmed_count = 0
        if result > 0:
            trimmed_result = round(result, -int(floor(log10(result)))+3) 
        else:
            trimmed_result = 0
        
        plotable_data.append( (time_bucket, count, trimmed_result) )
        if logr is not None:
            logr.debug("{0} {1:>8} {2}".format(time_bucket, trimmed_count, trimmed_result))  
    if return_queue is not None:
        return_queue.put_nowait((rule_name,plotable_data))
    return plotable_data

if __name__ == "__main__":
    
    logr = logging.getLogger("analyzer")
    if logr.handlers == []:
        fmtr = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s') 
        hndlr = logging.StreamHandler()
        hndlr.setFormatter(fmtr)
        logr.addHandler(hndlr) 

    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input-file",dest="input_file_name",default="output.pkl") 
    parser.add_argument("-d","--analyzed-file",dest="analyzed_data_file",default=None) 
    parser.add_argument("-c","--config-file",dest="config_file_name",default="config.cfg",help="get configuration from this file")
    parser.add_argument("-v","--verbose",dest="verbose",action="store_true",default=False)
    parser.add_argument("-s","--serializer",dest="serializer",default="pickle") 
    args = parser.parse_args()

    config = ConfigParser.SafeConfigParser()
    config.read(args.config_file_name)
    model_name = config.get("analyze","model_name")
    model_config = dict(config.items(model_name + "_model"))
    
    if args.verbose:
        logr.setLevel(logging.DEBUG)

    serializer = importlib.import_module(args.serializer)

    rule_name = config.get("rebin","rule_name")
    model = getattr(models,model_name)(config=model_config) 
    generator = serializer.load(open(args.input_file_name))[rule_name] 
    plotable_data = analyze(generator,model,None,None,logr)
    if args.analyzed_data_file is not None:
        serializer.dump({rule_name:plotable_data},open(args.analyzed_data_file,"w"))
