import sys
import os
try:
    import ujson as json  
except ImportError: 
    import json
import logging
from collections import defaultdict
from simple_n_grams.simple_n_grams import SimpleNGrams
import uuid
import datetime

def constant_factory():
    return (0, set([]))

logger = logging.getLogger("analysis")

def analyze_tweet(tweet,results):
    """ Add relevant data from 'tweet' to 'results'"""
    
    # simple tweet counter
    if 'tweet_count' not in results:
        results['tweet_count'] = 0
    results['tweet_count'] += 1

    # tweet body term counts
    if "body_term_count" not in results:
        results["body_term_count"] = SimpleNGrams(
                char_lower_cutoff=3
                ,n_grams=1
                ,tokenizer="twitter"
                )
    results["body_term_count"].add(tweet["body"])

    # which users are involved
    if "at_mentions" not in results:
        results["at_mentions"] = defaultdict(constant_factory)
    #if "mention_edges" not in results:
    #    results["mention_edges"] = {}
    for u in [x for x in tweet["twitter_entities"]["user_mentions"]]:
    	results["at_mentions"][u["id_str"]] = (results["at_mentions"][u["id_str"]][0] + 1, 
                results["at_mentions"][u["id_str"]][1] | set([u["screen_name"].lower()]))
        #if u not in results["mention_edges"]:
        #    results["mention_edges"][u["id_str"]] = {tweet["actor"]["id"][15:]: 1}
        #else:
        #    actor_id = tweet["actor"]["id"][15:]
        #    if actor_id not in results["mention_edges"][u["id_str"]]:
        #        results["mention_edges"][u["id_str"]][actor_id] = 1
        #    else:
        #        results["mention_edges"][u["id_str"]][actor_id] += 1
    
    if "inReplyTo" in tweet:
        if "in_reply_to" not in results:
            results["in_reply_to"] = defaultdict(int)
        results["in_reply_to"][tweet["inReplyTo"]["link"].split("/")[3].lower()] += 1

    if tweet["verb"] == "share":
        if "RT_of_user" not in results:
            results["RT_of_user"] = defaultdict(constant_factory)
        rt_of_name = tweet["object"]["actor"]["preferredUsername"].lower()
        rt_of_id = tweet["object"]["actor"]["id"][15:]
        results["RT_of_user"][rt_of_id] = (results["RT_of_user"][rt_of_id][0] + 1, 
                results["RT_of_user"][rt_of_id][1] | set([rt_of_name]))

    if "hashtags" not in results:
        results["hashtags"] = defaultdict(int)
    if "hashtags" in tweet["twitter_entities"]:
       for h in [x["text"].lower() for x in tweet["twitter_entities"]["hashtags"]]:
            results["hashtags"][h] += 1

    if "local_timeline" not in results:
        results["local_timeline"] = defaultdict(int)
    utcOffset = tweet["actor"]["utcOffset"]
    if utcOffset is not None:
        posted = tweet["postedTime"]
        hour_and_minute = (datetime.datetime.strptime(posted[0:16], "%Y-%m-%dT%H:%M") + 
                datetime.timedelta(seconds = int(utcOffset))).time().strftime("%H:%M")
        results["local_timeline"][hour_and_minute] += 1

    if "urls" not in results:
        results["urls"] = defaultdict(int)
    if "urls" in tweet["gnip"]:
        try:
            for url in [x["expanded_url"] for x in tweet["gnip"]["urls"]]:
                results["urls"][url.split("/")[2]] += 1
        except (KeyError,IndexError):
            pass

    if "user_ids_user_freq" not in results:
        results["user_ids_user_freq"] = defaultdict(int)
    results["user_ids_user_freq"][tweet["actor"]["id"][15:]] += 1

def analyze_bio(tweet,results):
    """ Add relevant per-user (rather than per Tweet) data to 'results'"""
   
    # simple tweet counter
    if 'tweet_count' not in results:
        results['tweet_count'] = 0
    results['tweet_count'] += 1

    if "bio_term_count" not in results:
        results["bio_term_count"] = SimpleNGrams(
                char_lower_cutoff=3
                ,n_grams=1
                ,tokenizer="twitter"
                )
    results["bio_term_count"].add(tweet["actor"]["summary"])

    #if "enrichments" in tweet:
        #if "age_and_gender_breakdown" not in results:
        #    results["age_and_gender_breakdown"] = defaultdict(int)
        #age = tweet["enrichments"]["UserAgeAndGender"]["age"]
        #gender = tweet["enrichments"]["UserAgeAndGender"]["gender"]
        #results["age_and_gender_breakdown"][(gender, age)] += 1

    #if "age_breakdown" not in results:
    #    results["age_breakdown"] = defaultdict(int)
    #results["age_breakdown"][tweet["enrichments"]["UserAgeAndGender"]["age"]] += 1

    if "profileLocations" in tweet["gnip"]:
        if "profile_locations_regions" not in results:
            results["profile_locations_regions"] = defaultdict(int)
        address = tweet["gnip"]["profileLocations"][0]["address"]
        if ("country" in address) and ("region" in address):
            results["profile_locations_regions"][address["country"] + " , " + address["region"]] += 1

    #if "profile_locations_cities" not in results:
    #    results["profile_locations_cities"] = defaultdict(int)

def analyze_user_ids(user_ids,results, groupings = None):
    """ call to Audience API goes here """
    import audience_api as api

    if groupings is not None:
        use_groupings = groupings
    else:
        grouping_dict = {"groupings": {
            "gender": {"group_by": ["user.gender"]}
            , "location_country": {"group_by": ["user.location.country"]}
            , "location_country_region": {"group_by": ["user.location.country", "user.location.region"]}
            , "interest": {"group_by": ["user.interest"]}
            , "tv_genre": {"group_by": ["user.tv.genre"]}
            , "device_os": {"group_by": ["user.device.os"]}
            , "device_network": {"group_by": ["user.device.network"]}
            , "language": {"group_by": ["user.language"]}}}
        use_groupings = json.dumps(grouping_dict)

    results['audience_api'] = api.query_users(list(user_ids), use_groupings)

def summarize_tweets(results):
    """ Generate summary items in results """
    pass

def summarize_audience(results):
    """ Generate summary items in results """
    pass
